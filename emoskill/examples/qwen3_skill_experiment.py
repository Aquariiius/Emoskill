from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from psychology_va import (
    ImageInput,
    ModelOutputParseError,
    PsychologyVAPipeline,
    Qwen3VLClient,
    load_skill_specs_from_directory,
)


DEFAULT_MODEL_PATH = "/home/u1120250383/dyp/models/qwen"
DEFAULT_PROJECT_ROOT = "/home/u1120250383/dcs/Emoskill_test"
DEFAULT_OUTPUT_DIR = "/home/u1120250383/dcs/Emoskill_test/script_output"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
REQUIRED_SKILL_SECTIONS = ("Purpose", "Output Format")
USE_WHEN_SECTION_NAMES = ("Use When", "Use-When Rules")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Qwen3-VL direct VA vs skill-routed VA experiment.")
    parser.add_argument("--model-path", default=os.environ.get("QWEN_MODEL_ROOT", DEFAULT_MODEL_PATH))
    parser.add_argument("--project-root", default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--skills-dir", default=str(REPO_ROOT / ".trae" / "skills"))
    parser.add_argument("--upload-dir", default=None)
    parser.add_argument("--output-dir", default=os.environ.get("SCRIPT_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--annotations-json",
        default=None,
        help=(
            "Optional human VA annotations JSON. If omitted, the script uses "
            "<upload-dir>/annotations.json when present."
        ),
    )
    parser.add_argument("--image", action="append", default=[], help="Specific image path. Can be repeated.")
    parser.add_argument(
        "--user-context",
        default="Analyze the image's valence-arousal state and choose the most suitable psychology skill.",
    )
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--max-pixels", type=int, default=1003520)
    parser.add_argument("--min-pixels", type=int, default=None)
    parser.add_argument("--device-map", default=os.environ.get("QWEN_DEVICE_MAP", "auto"))
    parser.add_argument("--include-duplicate-skills", action="store_true")
    parser.add_argument("--direct-only", action="store_true")
    parser.add_argument("--routed-only", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate SKILL.md parsing and image discovery without loading Qwen3-VL.",
    )
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="Print the loaded skill registry and exit before model inference.",
    )
    return parser.parse_args()


def find_images(upload_dir: Path, explicit_images: list[str]) -> list[Path]:
    if explicit_images:
        images = [Path(item).expanduser().resolve() for item in explicit_images]
        missing_images = [path for path in images if not path.exists()]
        if missing_images:
            raise FileNotFoundError(
                "Explicit image path(s) do not exist: "
                + ", ".join(str(path) for path in missing_images)
            )
        return images
    if not upload_dir.exists():
        raise FileNotFoundError(f"Upload directory does not exist: {upload_dir}")
    return sorted(
        path
        for path in upload_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def timed_call(func, *args, **kwargs) -> tuple[Any, float]:
    started = time.perf_counter()
    result = func(*args, **kwargs)
    return result, time.perf_counter() - started


def delta(skill_result: dict[str, Any], direct_result: dict[str, Any]) -> dict[str, float]:
    return {
        "valence_delta": round(float(skill_result["valence"]) - float(direct_result["valence"]), 4),
        "arousal_delta": round(float(skill_result["arousal"]) - float(direct_result["arousal"]), 4),
    }


def load_annotations(path: Path | None) -> dict[str, dict[str, float]]:
    if path is None or not path.exists():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, list):
        raise ValueError(f"Annotations JSON must contain a list: {path}")

    annotations: dict[str, dict[str, float]] = {}
    for row in raw:
        if not isinstance(row, dict):
            continue
        name = str(row.get("name") or "").strip()
        if not name:
            continue
        annotations[name] = {
            "valence": float(row["v"]),
            "arousal": float(row["a"]),
        }
    return annotations


def resolve_annotations_path(args: argparse.Namespace, upload_dir: Path) -> Path | None:
    if args.annotations_json:
        return Path(args.annotations_json).expanduser()
    candidate = upload_dir / "annotations.json"
    if candidate.exists():
        return candidate
    return None


def va_error(model_result: dict[str, Any], true_va: dict[str, float]) -> dict[str, float]:
    valence_delta = float(model_result["valence"]) - float(true_va["valence"])
    arousal_delta = float(model_result["arousal"]) - float(true_va["arousal"])
    return {
        "valence_delta": round(valence_delta, 6),
        "arousal_delta": round(arousal_delta, 6),
        "abs_valence_delta": round(abs(valence_delta), 6),
        "abs_arousal_delta": round(abs(arousal_delta), 6),
        "euclidean_distance": round(math.hypot(valence_delta, arousal_delta), 6),
    }


def summarize_error_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    def _mean(values: list[float]) -> float | None:
        if not values:
            return None
        return round(sum(values) / len(values), 6)

    summary: dict[str, Any] = {}
    for prefix in ("direct", "skill"):
        key = f"{prefix}_error"
        rows = [item[key] for item in results if key in item]
        summary[prefix] = {
            "count": len(rows),
            "mean_valence_delta": _mean([row["valence_delta"] for row in rows]),
            "mean_arousal_delta": _mean([row["arousal_delta"] for row in rows]),
            "mae_valence": _mean([row["abs_valence_delta"] for row in rows]),
            "mae_arousal": _mean([row["abs_arousal_delta"] for row in rows]),
            "mean_euclidean_distance": _mean([row["euclidean_distance"] for row in rows]),
        }
    return summary


def validate_skill_markdown(skill_specs: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in skill_specs:
        markdown = spec.raw_skill_markdown or ""
        missing_sections = [
            section
            for section in REQUIRED_SKILL_SECTIONS
            if f"## {section}" not in markdown
        ]
        has_use_when = any(f"## {section}" in markdown for section in USE_WHEN_SECTION_NAMES)
        if not has_use_when:
            missing_sections.append("Use When or Use-When Rules")
        rows.append(
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "frontmatter_name": spec.theory_family,
                "has_description": bool(spec.short_description),
                "selection_hint_count": len(spec.selection_hints),
                "analysis_step_count": len(spec.analysis_steps),
                "missing_sections": missing_sections,
                "source_path": spec.source_path,
            }
        )
    return rows


def print_skill_registry(skill_specs: list[Any]) -> None:
    print(f"Loaded {len(skill_specs)} skill(s) from SKILL.md:")
    for row in validate_skill_markdown(skill_specs):
        status = "ok" if not row["missing_sections"] else "missing " + ", ".join(row["missing_sections"])
        print(
            f"  - {row['skill_id']}: {row['display_name']} "
            f"(hints={row['selection_hint_count']}, steps={row['analysis_step_count']}, {status})"
        )


def write_outputs(output_dir: Path, payload: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"qwen3_skill_experiment_{stamp}.json"
    latest_json = output_dir / "qwen3_skill_experiment_latest.json"
    csv_path = output_dir / f"qwen3_skill_experiment_{stamp}.csv"
    latest_csv = output_dir / "qwen3_skill_experiment_latest.csv"

    body = json.dumps(payload, ensure_ascii=False, indent=2)
    json_path.write_text(body + "\n", encoding="utf-8")
    latest_json.write_text(body + "\n", encoding="utf-8")

    rows = []
    for item in payload.get("results", []):
        direct = item.get("direct_va") or {}
        routed = item.get("skill_va") or {}
        route = item.get("route") or {}
        item_delta = item.get("delta") or {}
        true_va = item.get("true_va") or {}
        direct_error = item.get("direct_error") or {}
        skill_error = item.get("skill_error") or {}
        rows.append(
            {
                "image": item.get("image"),
                "ok": item.get("ok"),
                "selected_skill": route.get("skill_id"),
                "route_confidence": route.get("confidence"),
                "true_valence": true_va.get("valence"),
                "true_arousal": true_va.get("arousal"),
                "direct_valence_score": direct.get("valence_score"),
                "direct_arousal_score": direct.get("arousal_score"),
                "direct_valence": direct.get("valence"),
                "direct_arousal": direct.get("arousal"),
                "skill_valence_score": routed.get("valence_score"),
                "skill_arousal_score": routed.get("arousal_score"),
                "skill_valence": routed.get("valence"),
                "skill_arousal": routed.get("arousal"),
                "skill_minus_direct_valence_delta": item_delta.get("valence_delta"),
                "skill_minus_direct_arousal_delta": item_delta.get("arousal_delta"),
                "direct_valence_delta": direct_error.get("valence_delta"),
                "direct_arousal_delta": direct_error.get("arousal_delta"),
                "direct_abs_valence_delta": direct_error.get("abs_valence_delta"),
                "direct_abs_arousal_delta": direct_error.get("abs_arousal_delta"),
                "direct_euclidean_distance": direct_error.get("euclidean_distance"),
                "skill_valence_delta": skill_error.get("valence_delta"),
                "skill_arousal_delta": skill_error.get("arousal_delta"),
                "skill_abs_valence_delta": skill_error.get("abs_valence_delta"),
                "skill_abs_arousal_delta": skill_error.get("abs_arousal_delta"),
                "skill_euclidean_distance": skill_error.get("euclidean_distance"),
                "direct_seconds": item.get("direct_seconds"),
                "route_seconds": item.get("route_seconds"),
                "skill_seconds": item.get("skill_seconds"),
                "error": item.get("error", ""),
                "parse_recovered": item.get("parse_recovered"),
                "raw_error_output": item.get("raw_error_output", ""),
            }
        )

    if rows:
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        latest_csv.write_text(csv_path.read_text(encoding="utf-8"), encoding="utf-8")

    return json_path, latest_json


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    project_root = Path(args.project_root).expanduser()
    upload_dir = Path(args.upload_dir).expanduser() if args.upload_dir else project_root / "uploads"
    output_dir = Path(args.output_dir).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    images = find_images(upload_dir, args.image)
    if not images:
        raise FileNotFoundError(f"No images found in {upload_dir}")
    annotations_path = resolve_annotations_path(args, upload_dir)
    annotations = load_annotations(annotations_path)

    skill_specs = load_skill_specs_from_directory(
        skills_dir,
        include_duplicate_frontmatter_names=args.include_duplicate_skills,
    )
    if args.dry_run or args.list_skills:
        print_skill_registry(skill_specs)
        print(f"Project root: {project_root}")
        print(f"Skills dir:   {skills_dir}")
        print(f"Upload dir:   {upload_dir}")
        print(f"Output dir:   {output_dir}")
        print(f"Annotations:  {annotations_path if annotations_path else '<none>'} ({len(annotations)})")
        print(f"Images:       {len(images)}")
        for image_path in images:
            print(f"  - {image_path}")
        if args.dry_run:
            return 0
        if args.list_skills:
            return 0

    if not args.model_path:
        print(
            "No Qwen3 model path configured. Pass --model-path or set QWEN_MODEL_ROOT. "
            "Use --dry-run to validate SKILL.md parsing without loading the model.",
            file=sys.stderr,
        )
        return 2

    client = Qwen3VLClient(
        model_name=args.model_path,
        device_map=args.device_map,
        max_new_tokens=args.max_new_tokens,
        min_pixels=args.min_pixels,
        max_pixels=args.max_pixels,
    )
    pipeline = PsychologyVAPipeline(llm_client=client, skill_specs=skill_specs)

    payload: dict[str, Any] = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "python": sys.executable,
        "model_path": args.model_path,
        "skills_dir": str(skills_dir),
        "upload_dir": str(upload_dir),
        "annotations_path": str(annotations_path) if annotations_path else None,
        "annotations_count": len(annotations),
        "score_scale": {
            "raw_score_min": 1,
            "raw_score_neutral": 5.5,
            "raw_score_max": 10,
            "normalization": "normalized = (score - 1) / 9",
            "valence_score": "1=very negative, 5.5=neutral, 10=very positive",
            "arousal_score": "1=very calm/deactivated, 5.5=moderate activation, 10=highly activated",
        },
        "args": vars(args),
        "skill_registry": [
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "short_description": spec.short_description,
                "selection_hints": spec.selection_hints,
                "analysis_steps": spec.analysis_steps,
                "source_path": spec.source_path,
            }
            for spec in skill_specs
        ],
        "skill_format_check": validate_skill_markdown(skill_specs),
        "images": [str(path) for path in images],
        "results": [],
    }

    print_skill_registry(skill_specs)
    print(f"Images: {len(images)}")
    if annotations_path:
        print(f"Annotations: {annotations_path} ({len(annotations)})")

    for index, image_path in enumerate(images, start=1):
        print(f"[{index}/{len(images)}] {image_path}")
        item: dict[str, Any] = {"image": str(image_path), "ok": False}
        true_va = annotations.get(image_path.name)
        if true_va:
            item["true_va"] = true_va
        image_input = ImageInput(image_path=str(image_path))
        try:
            direct_result = None
            if not args.routed_only:
                direct_result, direct_seconds = timed_call(
                    pipeline.analyze_direct,
                    image_input=image_input,
                    user_context=args.user_context,
                )
                item["direct_seconds"] = round(direct_seconds, 3)
                item["direct_va"] = direct_result.to_dict()
                if true_va:
                    item["direct_error"] = va_error(direct_result.to_dict(), true_va)
                print(
                    f"  direct: Vscore={direct_result.valence_score:.2f} "
                    f"Ascore={direct_result.arousal_score:.2f} "
                    f"(norm V={direct_result.valence:.3f} A={direct_result.arousal:.3f}) "
                    f"in {direct_seconds:.3f}s"
                )

            if not args.direct_only:
                route, route_seconds = timed_call(
                    pipeline.route_skill,
                    image_input=image_input,
                    user_context=args.user_context,
                )
                item["route_seconds"] = round(route_seconds, 3)
                item["route"] = route.to_dict()
                print(
                    f"  route: {route.skill_id} conf={route.confidence:.2f} in {route_seconds:.3f}s"
                )

                skill_result, skill_seconds = timed_call(
                    pipeline.analyze_with_route,
                    image_input=image_input,
                    route=route,
                    user_context=args.user_context,
                )
                item["skill_seconds"] = round(skill_seconds, 3)
                item["skill_va"] = skill_result.to_dict()
                if true_va:
                    item["skill_error"] = va_error(skill_result.to_dict(), true_va)
                raw_output = item["skill_va"].get("raw_model_output") or {}
                if raw_output.get("_parse_recovery"):
                    item["parse_recovered"] = raw_output["_parse_recovery"]
                    print(f"  parse: recovered from {raw_output['_parse_recovery']}")
                print(
                    f"  skill:  Vscore={skill_result.valence_score:.2f} "
                    f"Ascore={skill_result.arousal_score:.2f} "
                    f"(norm V={skill_result.valence:.3f} A={skill_result.arousal:.3f}) "
                    f"in {skill_seconds:.3f}s"
                )
                if direct_result is not None:
                    item["delta"] = delta(skill_result.to_dict(), direct_result.to_dict())

            item["ok"] = True
        except Exception as exc:
            item["error_type"] = type(exc).__name__
            item["error"] = str(exc)
            if isinstance(exc, ModelOutputParseError):
                item["raw_error_output"] = exc.raw_text
            item["traceback"] = traceback.format_exc()
            print(f"  ERROR: {type(exc).__name__}: {exc}")

        payload["results"].append(item)

    payload["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    payload["ok_count"] = sum(1 for item in payload["results"] if item.get("ok"))
    payload["error_summary"] = summarize_error_metrics(payload["results"])
    payload["summary"] = (
        f"OK images={payload['ok_count']}/{len(images)}; "
        f"elapsed={payload['elapsed_seconds']}s; skills={len(skill_specs)}"
    )
    json_path, latest_json = write_outputs(output_dir, payload)
    print(payload["summary"])
    print(f"Saved: {json_path}")
    print(f"Latest: {latest_json}")
    return 0 if payload["ok_count"] == len(images) else 1


if __name__ == "__main__":
    raise SystemExit(main())
