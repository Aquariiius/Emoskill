from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
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
    PsychologySkillSpec,
    PsychologyVAPipeline,
    Qwen3VLClient,
    RouteDecision,
    load_skill_specs_from_directory,
)
from psychology_va.prompts import (
    build_analysis_system_prompt,
    build_analysis_user_prompt,
    build_direct_va_system_prompt,
    build_direct_va_user_prompt,
    build_full_direct_va_system_prompt,
    build_full_routing_system_prompt,
    build_full_skill_analysis_system_prompt,
    build_routing_system_prompt,
    build_routing_user_prompt,
    build_skill_selection_system_prompt,
    build_skill_selection_user_prompt,
)
from psychology_va.schemas import NO_SPECIALIZED_SKILL_ID


DEFAULT_MODEL_PATH = "/home/u1120250383/dyp/models/qwen"
DEFAULT_PROJECT_ROOT = "/home/u1120250383/dcs/Emoskill_test"
DEFAULT_OUTPUT_DIR = "/home/u1120250383/dcs/Emoskill/script_output"
DEFAULT_IAPS_ALBUM_DIR = "/home/u1120250383/dcs/datasets/IAPS/Dataset"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
REQUIRED_SKILL_SECTIONS = (
    "Applicability Gate",
    "Visual Variables",
    "Inference Procedure",
    "VA Judgment",
    "Worked Example",
    "Output Contract",
)
MAX_ACTIVE_SKILL_BYTES = 6 * 1024
DEFAULT_DIAGNOSTIC_SKILLS = ("berlyne-arousal-pleasure", "cognitive-appraisal")
DEFAULT_IAPS_TRACE_CASE_IDS = (
    "7080",
    "9000",
    "4670",
    "2597",
    "5870",
    "5825",
    "6251",
    "2220",
    "4645",
    "9190",
    "4574",
    "5836",
    "2357",
    "7004",
    "2751",
    "6260",
)


def sanitize_slug(value: str, *, default: str = "dataset") -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {"-", "_"}:
            cleaned.append(char)
        else:
            cleaned.append("_")
    slug = "_".join(part for part in "".join(cleaned).split("_") if part)
    return slug or default


def dataset_slug(upload_dir: Path) -> str:
    normalized = str(upload_dir).replace("\\", "/").lower()
    if "iaps" in normalized:
        return "iaps"
    return sanitize_slug(upload_dir.name or upload_dir.parent.name)


def run_mode_slug(args: argparse.Namespace) -> str:
    if args.diagnose_skill_output:
        return "skill_diagnostic"
    if args.full_skill_analysis:
        return "iaps_full_skill"
    if args.trace_inference:
        return "iaps_trace"
    return "skill_experiment"


def run_output_dir(
    base_output_dir: Path,
    *,
    args: argparse.Namespace,
    upload_dir: Path,
    images: list[Path],
    worker_count: int,
    stamp: str | None = None,
) -> Path:
    stamp = stamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    mode = run_mode_slug(args)
    slug = f"{stamp}_{mode}_{dataset_slug(upload_dir)}_n{len(images)}_g{worker_count}"
    return base_output_dir / "runs" / slug


def update_latest_outputs(base_output_dir: Path, run_dir: Path, *, mode: str) -> Path:
    latest_dir = base_output_dir / "latest" / mode
    latest_dir.mkdir(parents=True, exist_ok=True)
    for artifact in latest_dir.iterdir():
        if artifact.is_file():
            artifact.unlink()
    for artifact in run_dir.iterdir():
        if artifact.is_file() and "latest" in artifact.name:
            shutil.copy2(artifact, latest_dir / artifact.name)
    (latest_dir / "RUN_DIR.txt").write_text(str(run_dir) + "\n", encoding="utf-8")
    return latest_dir


def attach_output_paths(payload: dict[str, Any], base_output_dir: Path, run_dir: Path, *, mode: str) -> None:
    payload["output"] = {
        "layout": "runs/latest",
        "mode": mode,
        "base_dir": str(base_output_dir),
        "run_dir": str(run_dir),
        "latest_dir": str(base_output_dir / "latest" / mode),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Qwen3-VL direct VA vs skill-routed VA experiment.")
    parser.add_argument("--model-path", default=os.environ.get("QWEN_MODEL_ROOT", DEFAULT_MODEL_PATH))
    parser.add_argument("--project-root", default=DEFAULT_PROJECT_ROOT)
    parser.add_argument("--skills-dir", default=str(REPO_ROOT / ".trae" / "skills"))
    parser.add_argument("--upload-dir", default=None)
    parser.add_argument(
        "--album-path",
        default=None,
        help=(
            "Image album directory. Alias for --upload-dir. "
            f"IAPS server path: {DEFAULT_IAPS_ALBUM_DIR}"
        ),
    )
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
        "--image-list",
        action="append",
        default=[],
        help="Text file with one image path per line. Can be repeated.",
    )
    parser.add_argument(
        "--iaps-case-id",
        action="append",
        default=[],
        help=(
            "IAPS image id or filename under --album-path/--upload-dir, e.g. 7080 or 7080.jpg. "
            "Can be repeated; comma/space separated values are also accepted."
        ),
    )
    parser.add_argument(
        "--iaps-trace-cases",
        action="store_true",
        help="Use the default 16 IAPS case ids for detailed inference tracing.",
    )
    parser.add_argument(
        "--user-context",
        default="Analyze the image's valence-arousal state and choose the most suitable psychology skill.",
    )
    parser.add_argument("--max-new-tokens", type=int, default=None)
    parser.add_argument(
        "--full-skill-token-budget",
        type=int,
        default=8192,
        choices=(8192, 16384),
        help="Default max_new_tokens for full-skill inference when --max-new-tokens is not set.",
    )
    parser.add_argument("--max-pixels", type=int, default=1003520)
    parser.add_argument("--min-pixels", type=int, default=None)
    parser.add_argument("--device-map", default=os.environ.get("QWEN_DEVICE_MAP", "auto"))
    parser.add_argument("--include-duplicate-skills", action="store_true")
    parser.add_argument("--direct-only", action="store_true")
    parser.add_argument("--routed-only", action="store_true")
    parser.add_argument(
        "--multi-skill-candidates",
        action="store_true",
        help=(
            "When routing returns multiple plausible skills, run analysis for up to "
            "--max-candidate-skills candidates and let the model select the final score."
        ),
    )
    parser.add_argument(
        "--max-candidate-skills",
        type=int,
        default=2,
        help="Maximum routed candidate skills to analyze when --multi-skill-candidates is enabled.",
    )
    parser.add_argument(
        "--parallel-gpus",
        default=None,
        help="Comma-separated GPU ids for data-parallel sharded inference, e.g. 0,1,2,3.",
    )
    parser.add_argument(
        "--images-per-gpu",
        type=int,
        default=None,
        help="Limit parallel runs to this many images per GPU, useful for small diagnostics.",
    )
    parser.add_argument(
        "--four-gpu",
        action="store_true",
        help="Shortcut for --parallel-gpus 0,1,2,3.",
    )
    parser.add_argument("--parallel-worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--worker-id", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument("--worker-count", type=int, default=None, help=argparse.SUPPRESS)
    parser.add_argument(
        "--diagnose-skill-output",
        action="store_true",
        help="Run a small forced-skill output-schema diagnostic instead of the full experiment.",
    )
    parser.add_argument(
        "--diagnostic-skill",
        action="append",
        default=[],
        help=(
            "Skill id to force during --diagnose-skill-output. "
            "Can be repeated. Defaults to berlyne-arousal-pleasure and cognitive-appraisal."
        ),
    )
    parser.add_argument(
        "--trace-inference",
        action="store_true",
        help=(
            "Record detailed direct/routing/skill call traces, including prompts, parsed payloads, "
            "raw model text, and normalized results."
        ),
    )
    parser.add_argument(
        "--full-skill-analysis",
        action="store_true",
        help=(
            "Use complete SKILL.md content and long-form structured inference prompts for traced calls. "
            "This implies --trace-inference."
        ),
    )
    parser.add_argument(
        "--full-skill-inference",
        action="store_true",
        help=(
            "One-shot mode for the 16 selected IAPS cases: implies --iaps-trace-cases, "
            "--trace-inference, --full-skill-analysis, and Markdown inference output."
        ),
    )
    parser.add_argument(
        "--write-inference-markdown",
        action="store_true",
        help="Write a readable Markdown file with direct/routing/skill inference and VA scores.",
    )
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
    args = parser.parse_args()
    if args.four_gpu and not args.parallel_gpus:
        args.parallel_gpus = "0,1,2,3"
    if args.max_candidate_skills <= 0:
        raise ValueError("--max-candidate-skills must be a positive integer.")
    if args.full_skill_inference:
        args.iaps_trace_cases = True
        args.trace_inference = True
        args.full_skill_analysis = True
        args.write_inference_markdown = True
    if args.full_skill_analysis:
        args.trace_inference = True
    if args.max_new_tokens is None:
        args.max_new_tokens = args.full_skill_token_budget if args.full_skill_analysis else 512
    return args


def resolve_upload_dir(args: argparse.Namespace) -> Path:
    if args.upload_dir and args.album_path:
        upload_dir = Path(args.upload_dir).expanduser()
        album_path = Path(args.album_path).expanduser()
        if upload_dir != album_path:
            raise ValueError("--upload-dir and --album-path point to different directories.")
        return upload_dir
    if args.upload_dir:
        return Path(args.upload_dir).expanduser()
    if args.album_path:
        return Path(args.album_path).expanduser()
    return Path(args.project_root).expanduser() / "uploads"


def find_images(upload_dir: Path, explicit_images: list[str], image_lists: list[str] | None = None) -> list[Path]:
    image_list_entries = load_image_list_entries(image_lists or [])
    if explicit_images or image_list_entries:
        images = [Path(item).expanduser().resolve() for item in [*image_list_entries, *explicit_images]]
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


def resolve_experiment_images(args: argparse.Namespace, upload_dir: Path) -> list[Path]:
    case_ids = collect_iaps_case_ids(args, upload_dir)
    if case_ids:
        return resolve_iaps_case_images(upload_dir, case_ids)
    return find_images(upload_dir, args.image, args.image_list)


def collect_iaps_case_ids(args: argparse.Namespace, upload_dir: Path) -> list[str]:
    case_ids: list[str] = []
    if args.iaps_trace_cases:
        case_ids.extend(DEFAULT_IAPS_TRACE_CASE_IDS)
    for raw_value in args.iaps_case_id:
        for token in raw_value.replace(",", " ").split():
            stripped = token.strip()
            if stripped:
                case_ids.extend(split_iaps_case_token(upload_dir, stripped))

    seen: set[str] = set()
    unique_ids: list[str] = []
    for case_id in case_ids:
        if case_id not in seen:
            unique_ids.append(case_id)
            seen.add(case_id)
    return unique_ids


def split_iaps_case_token(upload_dir: Path, token: str) -> list[str]:
    clean = token[:-4] if token.lower().endswith(".jpg") else token
    exact_path = upload_dir / f"{clean}.jpg"
    if exact_path.exists() or not clean.isdigit() or len(clean) <= 4:
        return [clean]
    if len(clean) % 4 == 0:
        return [clean[index : index + 4] for index in range(0, len(clean), 4)]
    return [clean]


def resolve_iaps_case_images(upload_dir: Path, case_ids: list[str]) -> list[Path]:
    if not upload_dir.exists():
        raise FileNotFoundError(f"Upload directory does not exist: {upload_dir}")

    images: list[Path] = []
    missing: list[str] = []
    for case_id in case_ids:
        candidates = [
            upload_dir / case_id,
            upload_dir / f"{case_id}.jpg",
            upload_dir / f"{case_id}.jpeg",
            upload_dir / f"{case_id}.png",
        ]
        found = next((path for path in candidates if path.exists()), None)
        if found is None:
            missing.append(case_id)
        else:
            images.append(found.resolve())

    if missing:
        raise FileNotFoundError(
            "IAPS case image(s) not found under "
            f"{upload_dir}: {', '.join(missing)}"
        )
    return images


def load_image_list_entries(image_lists: list[str]) -> list[str]:
    entries: list[str] = []
    for image_list in image_lists:
        path = Path(image_list).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"Image list does not exist: {path}")
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                entries.append(stripped)
    return entries


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
        missing_sections = [] if not spec.routing_enabled else [
            section for section in REQUIRED_SKILL_SECTIONS if f"## {section}" not in markdown
        ]
        if spec.routing_enabled:
            size_bytes = len(markdown.encode("utf-8"))
            if size_bytes > MAX_ACTIVE_SKILL_BYTES:
                missing_sections.append(
                    f"size {size_bytes}B exceeds {MAX_ACTIVE_SKILL_BYTES}B"
                )
            if len(spec.analysis_steps) < 4:
                missing_sections.append("Inference Procedure needs at least 4 numbered steps")
            if not spec.routing_card.get("use_when"):
                missing_sections.append("Applicability Gate REQUIRED")
            if not spec.routing_card.get("do_not_use_when"):
                missing_sections.append("Applicability Gate REJECT")
        rows.append(
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "frontmatter_name": spec.theory_family,
                "has_description": bool(spec.short_description),
                "selection_hint_count": len(spec.selection_hints),
                "analysis_step_count": len(spec.analysis_steps),
                "size_bytes": len(markdown.encode("utf-8")),
                "routing_enabled": spec.routing_enabled,
                "missing_sections": missing_sections,
                "source_path": spec.source_path,
            }
        )
    return rows


def print_skill_registry(skill_specs: list[Any]) -> None:
    print(f"Loaded {len(skill_specs)} skill(s) from SKILL.md:")
    for row in validate_skill_markdown(skill_specs):
        status = (
            "excluded from main routing"
            if not row["routing_enabled"]
            else "ok" if not row["missing_sections"] else "missing " + ", ".join(row["missing_sections"])
        )
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
        selection = item.get("skill_selection") or {}
        item_delta = item.get("delta") or {}
        true_va = item.get("true_va") or {}
        direct_error = item.get("direct_error") or {}
        skill_error = item.get("skill_error") or {}
        rows.append(
            {
                "image": item.get("image"),
                "worker_id": item.get("worker_id"),
                "gpu_id": item.get("gpu_id"),
                "ok": item.get("ok"),
                "route_primary_skill": route.get("skill_id"),
                "selected_skill": selection.get("selected_skill_id") or route.get("skill_id"),
                "candidate_skill_ids": json.dumps(
                    item.get("candidate_skill_ids")
                    or route.get("candidate_skill_ids")
                    or [],
                    ensure_ascii=False,
                ),
                "candidate_skill_count": len(item.get("candidate_skill_analyses") or []),
                "selection_reason": selection.get("reason", ""),
                "selection_fallback": selection.get("fallback", ""),
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
                "skill_applicability": routed.get("applicability"),
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


def write_diagnostic_outputs(output_dir: Path, payload: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = output_dir / f"qwen3_skill_diagnostic_{stamp}.json"
    latest_json = output_dir / "qwen3_skill_diagnostic_latest.json"
    csv_path = output_dir / f"qwen3_skill_diagnostic_{stamp}.csv"
    latest_csv = output_dir / "qwen3_skill_diagnostic_latest.csv"

    body = json.dumps(payload, ensure_ascii=False, indent=2)
    json_path.write_text(body + "\n", encoding="utf-8")
    latest_json.write_text(body + "\n", encoding="utf-8")

    rows = []
    for item in payload.get("results", []):
        normalized = item.get("normalized_va") or {}
        rows.append(
            {
                "image": item.get("image"),
                "worker_id": item.get("worker_id"),
                "gpu_id": item.get("gpu_id"),
                "skill_id": item.get("skill_id"),
                "ok": item.get("ok"),
                "classification": item.get("classification"),
                "payload_keys": json.dumps(item.get("payload_keys") or [], ensure_ascii=False),
                "valence_score": normalized.get("valence_score"),
                "arousal_score": normalized.get("arousal_score"),
                "parse_recovered": item.get("parse_recovered"),
                "error_type": item.get("error_type", ""),
                "error": item.get("error", ""),
                "normalization_error_type": item.get("normalization_error_type", ""),
                "normalization_error": item.get("normalization_error", ""),
                "raw_text_preview": preview_text(str(item.get("raw_model_text") or "")),
            }
        )

    if rows:
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        latest_csv.write_text(csv_path.read_text(encoding="utf-8"), encoding="utf-8")

    return json_path, latest_json


def write_trace_latest(output_dir: Path, payload: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_latest = output_dir / "qwen3_iaps_case_trace_latest.json"
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    trace_latest.write_text(body + "\n", encoding="utf-8")
    return trace_latest


def write_full_skill_latest(output_dir: Path, payload: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    latest = output_dir / "qwen3_iaps_full_skill_inference_latest.json"
    body = json.dumps(payload, ensure_ascii=False, indent=2)
    latest.write_text(body + "\n", encoding="utf-8")
    return latest


def write_inference_markdown(output_dir: Path, payload: dict[str, Any]) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "qwen3_iaps_full_skill_inference" if payload.get("full_skill_analysis") else "qwen3_iaps_case_inference"
    md_path = output_dir / f"{prefix}_{stamp}.md"
    latest_md = output_dir / f"{prefix}_latest.md"

    lines = [
        f"# {prefix}",
        "",
        f"- time: {payload.get('time')}",
        f"- model_path: {payload.get('model_path')}",
        f"- images: {len(payload.get('results') or [])}",
        f"- max_new_tokens: {(payload.get('args') or {}).get('max_new_tokens')}",
        f"- full_skill_analysis: {payload.get('full_skill_analysis')}",
        "",
    ]

    for item in payload.get("results", []):
        image_path = Path(str(item.get("image") or ""))
        case_label = image_path.name or str(item.get("image") or "<unknown image>")
        route = item.get("route") or {}
        lines.extend(
            [
                f"## {case_label}",
                "",
                f"- image: `{item.get('image')}`",
                f"- ok: {item.get('ok')}",
                f"- selected_skill: `{route.get('skill_id', '')}`",
                f"- route_confidence: {route.get('confidence', '')}",
                f"- DirectVA: {format_va_for_markdown(item.get('direct_va'))}",
                f"- SkillVA: {format_va_for_markdown(item.get('skill_va'))}",
                "",
            ]
        )
        selection = item.get("skill_selection") or {}
        if selection:
            lines.extend(
                [
                    "### Final skill selection",
                    "",
                    f"- selected_skill_id: `{selection.get('selected_skill_id', '')}`",
                    f"- confidence: {selection.get('confidence', '')}",
                    f"- fallback: {selection.get('fallback', '')}",
                    f"- reason: {selection.get('reason', '')}",
                    "",
                ]
            )
        candidates = item.get("candidate_skill_analyses") or []
        if candidates:
            lines.extend(["### Candidate skill analyses", ""])
            for candidate in candidates:
                candidate_va = candidate.get("skill_va") or {}
                raw_output = candidate_va.get("raw_model_output") or {}
                lines.extend(
                    [
                        f"#### {candidate.get('candidate_index', '')}. {candidate.get('skill_id', '')}",
                        "",
                        f"- ok: {candidate.get('ok')}",
                        f"- VA: {format_va_for_markdown(candidate_va)}",
                        f"- seconds: {candidate.get('seconds', '')}",
                        "",
                    ]
                )
                if candidate.get("ok"):
                    lines.extend([render_trace_payload_for_markdown("skill_analysis", {"raw_model_payload": raw_output}), ""])
                else:
                    lines.extend([f"{candidate.get('error_type', '')}: {candidate.get('error', '')}", ""])
        if not item.get("ok"):
            lines.extend(
                [
                    "### Error",
                    "",
                    f"{item.get('error_type', '')}: {item.get('error', '')}",
                    "",
                ]
            )

        for step, title in (
            ("direct_va_baseline", "Direct inference"),
            ("route_skill", "Routing inference"),
            ("skill_analysis", "Skill inference"),
        ):
            entry = trace_entry(item, step)
            if not entry:
                continue
            lines.extend([f"### {title}", "", trace_stats_for_markdown(entry), ""])
            payload_text = render_trace_payload_for_markdown(step, entry)
            lines.extend([payload_text, ""])

    body = "\n".join(lines).rstrip() + "\n"
    md_path.write_text(body, encoding="utf-8")
    latest_md.write_text(body, encoding="utf-8")
    return md_path, latest_md


def format_va_for_markdown(result: Any) -> str:
    if not isinstance(result, dict):
        return ""
    valence_score = result.get("valence_score")
    arousal_score = result.get("arousal_score")
    valence = result.get("valence")
    arousal = result.get("arousal")
    return (
        f"Vscore={format_number(valence_score)}; "
        f"Ascore={format_number(arousal_score)}; "
        f"normV={format_number(valence)}; "
        f"normA={format_number(arousal)}"
    )


def format_number(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        return f"{float(value):.3f}"
    except (TypeError, ValueError):
        return str(value)


def trace_entry(item: dict[str, Any], step: str) -> dict[str, Any] | None:
    for entry in item.get("inference_trace") or []:
        if entry.get("step") == step:
            return entry
    return None


def trace_stats_for_markdown(entry: dict[str, Any]) -> str:
    return (
        f"`seconds={entry.get('seconds', '')}`, "
        f"`input_tokens={entry.get('input_tokens', '')}`, "
        f"`generated_tokens={entry.get('generated_tokens', '')}`, "
        f"`hit_limit={entry.get('generation_hit_limit', '')}`"
    )


def render_trace_payload_for_markdown(step: str, entry: dict[str, Any]) -> str:
    payload = entry.get("raw_model_payload")
    if not isinstance(payload, dict):
        raw_text = str(entry.get("raw_model_text") or "").strip()
        return raw_text or "<no model payload>"

    if step == "route_skill":
        fields = [
            ("reason", "Final decision"),
            ("observed_cues", "Observed cues"),
            ("candidate_skill_ids", "Candidate skills"),
            ("visual_skill_match", "Visual skill match"),
            ("selection_reasoning", "Selection reasoning"),
            ("alternative_skill_ids", "Alternative skills"),
            ("rejected_alternatives", "Rejected alternatives"),
            ("uncertainty", "Uncertainty"),
        ]
    elif step in {"skill_analysis", "candidate_skill_analysis"}:
        fields = [
            ("summary", "Summary"),
            ("applicability", "Applicability"),
            ("visual_evidence", "Visual evidence"),
            ("evidence", "Evidence"),
            ("construct_estimates", "Construct estimates"),
            ("skill_procedure_trace", "Skill procedure trace"),
            ("context_modifiers", "Context modifiers"),
            ("va_judgment", "VA judgment"),
            ("uncertainty", "Uncertainty"),
            ("inference_summary", "Inference summary"),
        ]
    else:
        fields = [
            ("summary", "Summary"),
            ("visual_observations", "Visual observations"),
            ("evidence", "Evidence"),
            ("matched_emotions", "Matched emotions"),
            ("affect_interpretation", "Affect interpretation"),
            ("va_mapping_reasoning", "VA mapping reasoning"),
            ("uncertainty", "Uncertainty"),
            ("reasoning_trace", "Reasoning trace"),
        ]

    chunks: list[str] = []
    for key, label in fields:
        value = payload.get(key)
        if empty_markdown_value(value):
            continue
        chunks.append(f"**{label}:**\n{markdown_value(value)}")

    if chunks:
        return "\n\n".join(chunks)
    return "```json\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n```"


def empty_markdown_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def markdown_value(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        if not value:
            return ""
        return "\n".join(f"- {markdown_inline(item)}" for item in value)
    if isinstance(value, dict):
        if not value:
            return ""
        return "\n".join(f"- {key}: {markdown_inline(nested)}" for key, nested in value.items())
    return str(value)


def markdown_inline(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return "; ".join(f"{key}: {markdown_inline(nested)}" for key, nested in value.items())
    if isinstance(value, list):
        return ", ".join(markdown_inline(item) for item in value)
    return str(value)


def preview_text(text: str, limit: int = 500) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "... [truncated]"


def parse_gpu_ids(value: str | None) -> list[str]:
    if not value:
        return []
    gpu_ids = [item.strip() for item in value.split(",") if item.strip()]
    if not gpu_ids:
        raise ValueError("--parallel-gpus did not contain any GPU ids.")
    return gpu_ids


def split_images_for_workers(images: list[Path], worker_count: int) -> list[list[Path]]:
    shards: list[list[Path]] = [[] for _ in range(worker_count)]
    for index, image_path in enumerate(images):
        shards[index % worker_count].append(image_path)
    return shards


def write_image_list(path: Path, images: list[Path]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(str(image_path) for image_path in images) + "\n", encoding="utf-8")


def format_duration(seconds: float) -> str:
    total_seconds = max(0, int(round(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_progress_line(
    *,
    completed: int,
    total: int,
    elapsed_seconds: float,
    active_workers: int | None = None,
    width: int = 28,
) -> str:
    fraction = (completed / total) if total else 1.0
    filled = min(width, max(0, int(round(width * fraction))))
    bar = "#" * filled + "-" * (width - filled)
    elapsed = max(0.0, elapsed_seconds)
    if completed > 0 and elapsed > 0:
        rate = completed / elapsed
        eta = (total - completed) / rate if rate > 0 else 0.0
        rate_text = f"{rate:.3f} img/s"
        eta_text = format_duration(eta)
    else:
        rate_text = "waiting for first image"
        eta_text = "--:--:--"
    worker_text = f" | workers {active_workers}" if active_workers is not None else ""
    return (
        f"Progress [{bar}] {completed}/{total} ({fraction * 100:5.1f}%)"
        f" | elapsed {format_duration(elapsed)} | {rate_text} | ETA {eta_text}{worker_text}"
    )


def write_worker_progress(
    output_dir: Path,
    *,
    completed: int,
    total: int,
    last_image: str = "",
    last_ok: bool | None = None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = output_dir / "progress.json"
    temp_path = output_dir / "progress.json.tmp"
    payload = {
        "completed": completed,
        "total": total,
        "last_image": last_image,
        "last_ok": last_ok,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }
    temp_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    temp_path.replace(progress_path)


def read_worker_progress(output_dir: str | Path) -> dict[str, Any]:
    progress_path = Path(output_dir) / "progress.json"
    try:
        payload = json.loads(progress_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def monitor_parallel_progress(
    workers: list[dict[str, Any]],
    *,
    total_images: int,
    started: float,
    poll_seconds: float = 2.0,
) -> None:
    try:
        from tqdm.auto import tqdm
    except ImportError:
        tqdm = None

    if tqdm is not None:
        last_completed = 0
        with tqdm(total=total_images, desc="Images", unit="img", dynamic_ncols=True) as progress_bar:
            while True:
                completed = sum(
                    min(int(progress.get("completed") or 0), int(worker["image_count"]))
                    for worker in workers
                    for progress in [read_worker_progress(worker["output_dir"])]
                )
                active_workers = sum(1 for worker in workers if worker["process"].poll() is None)
                if completed > last_completed:
                    progress_bar.update(completed - last_completed)
                    last_completed = completed
                progress_bar.set_postfix(
                    workers=active_workers,
                    elapsed=format_duration(time.perf_counter() - started),
                    refresh=True,
                )
                if active_workers == 0:
                    return
                time.sleep(poll_seconds)

    previous_width = 0
    while True:
        completed = sum(
            min(int(progress.get("completed") or 0), int(worker["image_count"]))
            for worker in workers
            for progress in [read_worker_progress(worker["output_dir"])]
        )
        active_workers = sum(1 for worker in workers if worker["process"].poll() is None)
        line = format_progress_line(
            completed=completed,
            total=total_images,
            elapsed_seconds=time.perf_counter() - started,
            active_workers=active_workers,
        )
        padding = " " * max(0, previous_width - len(line))
        print(f"\r{line}{padding}", end="", flush=True)
        previous_width = len(line)
        if active_workers == 0:
            print()
            return
        time.sleep(poll_seconds)


def image_order_keys(image_path: Path) -> list[str]:
    raw = str(image_path)
    return [raw, raw.replace("\\", "/"), image_path.as_posix()]


def run_parallel(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    gpu_ids = parse_gpu_ids(args.parallel_gpus)
    project_root = Path(args.project_root).expanduser()
    upload_dir = resolve_upload_dir(args)
    base_output_dir = Path(args.output_dir).expanduser()
    images = resolve_experiment_images(args, upload_dir)
    if not images:
        raise FileNotFoundError(f"No images found in {upload_dir}")
    if args.images_per_gpu is not None:
        if args.images_per_gpu <= 0:
            raise ValueError("--images-per-gpu must be a positive integer.")
        images = images[: len(gpu_ids) * args.images_per_gpu]

    shards = split_images_for_workers(images, len(gpu_ids))
    active_shards = [
        (worker_id, gpu_ids[worker_id], shard)
        for worker_id, shard in enumerate(shards)
        if shard
    ]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = run_output_dir(
        base_output_dir,
        args=args,
        upload_dir=upload_dir,
        images=images,
        worker_count=len(active_shards),
        stamp=stamp,
    )
    parallel_dir = run_dir / "workers"
    parallel_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"Parallel run: images={len(images)}, workers={len(active_shards)}, "
        f"gpus={','.join(gpu_id for _, gpu_id, _ in active_shards)}"
    )
    print(f"Album: {upload_dir}")
    print(f"Output run: {run_dir}")
    print(f"Worker artifacts: {parallel_dir}")

    processes: list[dict[str, Any]] = []
    for worker_id, gpu_id, shard in active_shards:
        worker_dir = parallel_dir / f"worker_{worker_id}_gpu_{gpu_id}"
        image_list_path = parallel_dir / f"worker_{worker_id}_images.txt"
        log_path = parallel_dir / f"worker_{worker_id}_gpu_{gpu_id}.log"
        write_image_list(image_list_path, shard)

        command = build_worker_command(
            args=args,
            project_root=project_root,
            upload_dir=upload_dir,
            worker_dir=worker_dir,
            image_list_path=image_list_path,
            worker_id=worker_id,
            worker_count=len(active_shards),
        )
        env = os.environ.copy()
        env["CUDA_VISIBLE_DEVICES"] = gpu_id
        env["PYTHONUNBUFFERED"] = "1"
        log_handle = log_path.open("w", encoding="utf-8")
        process = subprocess.Popen(
            command,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            env=env,
        )
        processes.append(
            {
                "worker_id": worker_id,
                "gpu_id": gpu_id,
                "image_count": len(shard),
                "output_dir": str(worker_dir),
                "image_list": str(image_list_path),
                "log_path": str(log_path),
                "process": process,
                "log_handle": log_handle,
            }
        )
        print(f"  worker {worker_id}: gpu={gpu_id}, images={len(shard)}, log={log_path}")

    if args.diagnose_skill_output:
        for worker in processes:
            worker["process"].wait()
    else:
        monitor_parallel_progress(
            processes,
            total_images=len(images),
            started=started,
        )

    for worker in processes:
        return_code = worker["process"].wait()
        worker["log_handle"].close()
        worker["return_code"] = return_code
        status = "ok" if return_code == 0 else f"exit={return_code}"
        print(
            f"  worker {worker['worker_id']} finished: {status}, "
            f"images={worker['image_count']}, log={worker['log_path']}"
        )

    worker_payloads: list[tuple[dict[str, Any], dict[str, Any]]] = []
    missing_outputs: list[str] = []
    for worker in processes:
        latest_name = (
            "qwen3_skill_diagnostic_latest.json"
            if args.diagnose_skill_output
            else "qwen3_skill_experiment_latest.json"
        )
        latest_json = Path(worker["output_dir"]) / latest_name
        worker["latest_json"] = str(latest_json)
        if not latest_json.exists():
            missing_outputs.append(str(latest_json))
            continue
        payload = json.loads(latest_json.read_text(encoding="utf-8"))
        worker_payloads.append((worker, payload))

    if not worker_payloads:
        print("No worker output JSON files were produced.", file=sys.stderr)
        for missing_output in missing_outputs:
            print(f"Missing: {missing_output}", file=sys.stderr)
        return 1

    if args.diagnose_skill_output:
        merged_payload = merge_diagnostic_worker_payloads(
            args=args,
            images=images,
            upload_dir=upload_dir,
            worker_payloads=worker_payloads,
            workers=processes,
            started=started,
            parallel_dir=parallel_dir,
        )
    else:
        merged_payload = merge_worker_payloads(
            args=args,
            images=images,
            upload_dir=upload_dir,
            worker_payloads=worker_payloads,
            workers=processes,
            started=started,
            parallel_dir=parallel_dir,
        )
    if missing_outputs:
        merged_payload["missing_worker_outputs"] = missing_outputs

    mode = run_mode_slug(args)
    attach_output_paths(merged_payload, base_output_dir, run_dir, mode=mode)
    if args.diagnose_skill_output:
        json_path, latest_json = write_diagnostic_outputs(run_dir, merged_payload)
    else:
        json_path, latest_json = write_outputs(run_dir, merged_payload)
        if args.trace_inference:
            trace_latest = write_trace_latest(run_dir, merged_payload)
            print(f"Trace latest: {trace_latest}")
            if args.full_skill_analysis:
                full_skill_latest = write_full_skill_latest(run_dir, merged_payload)
                print(f"Full-skill latest: {full_skill_latest}")
            if args.write_inference_markdown:
                md_path, latest_md = write_inference_markdown(run_dir, merged_payload)
                print(f"Inference Markdown: {md_path}")
                print(f"Inference Markdown latest: {latest_md}")
    latest_dir = update_latest_outputs(base_output_dir, run_dir, mode=mode)
    print(merged_payload["summary"])
    print(f"Merged: {json_path}")
    print(f"Latest: {latest_json}")
    print(f"Latest dir: {latest_dir}")
    if missing_outputs:
        return 1
    if args.diagnose_skill_output:
        return 0
    return 0 if merged_payload["ok_count"] == len(images) else 1


def build_worker_command(
    *,
    args: argparse.Namespace,
    project_root: Path,
    upload_dir: Path,
    worker_dir: Path,
    image_list_path: Path,
    worker_id: int,
    worker_count: int,
) -> list[str]:
    command = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--model-path",
        str(args.model_path),
        "--project-root",
        str(project_root),
        "--skills-dir",
        str(Path(args.skills_dir).expanduser()),
        "--upload-dir",
        str(upload_dir),
        "--output-dir",
        str(worker_dir),
        "--image-list",
        str(image_list_path),
        "--user-context",
        str(args.user_context),
        "--max-new-tokens",
        str(args.max_new_tokens),
        "--max-pixels",
        str(args.max_pixels),
        "--device-map",
        str(args.device_map),
        "--max-candidate-skills",
        str(args.max_candidate_skills),
        "--parallel-worker",
        "--worker-id",
        str(worker_id),
        "--worker-count",
        str(worker_count),
    ]
    if args.min_pixels is not None:
        command.extend(["--min-pixels", str(args.min_pixels)])
    if args.annotations_json:
        command.extend(["--annotations-json", str(args.annotations_json)])
    if args.include_duplicate_skills:
        command.append("--include-duplicate-skills")
    if args.direct_only:
        command.append("--direct-only")
    if args.routed_only:
        command.append("--routed-only")
    if args.multi_skill_candidates:
        command.append("--multi-skill-candidates")
    if args.diagnose_skill_output:
        command.append("--diagnose-skill-output")
        for skill_id in args.diagnostic_skill:
            command.extend(["--diagnostic-skill", str(skill_id)])
    if args.trace_inference:
        command.append("--trace-inference")
    if args.full_skill_analysis:
        command.append("--full-skill-analysis")
    if args.write_inference_markdown:
        command.append("--write-inference-markdown")
    return command


def merge_worker_payloads(
    *,
    args: argparse.Namespace,
    images: list[Path],
    upload_dir: Path,
    worker_payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    workers: list[dict[str, Any]],
    started: float,
    parallel_dir: Path,
) -> dict[str, Any]:
    first_payload = worker_payloads[0][1]
    image_order = {
        key: index
        for index, image_path in enumerate(images)
        for key in image_order_keys(image_path)
    }
    results: list[dict[str, Any]] = []
    for worker, payload in worker_payloads:
        for item in payload.get("results", []):
            merged_item = dict(item)
            merged_item["worker_id"] = worker["worker_id"]
            merged_item["gpu_id"] = worker["gpu_id"]
            results.append(merged_item)
    results.sort(
        key=lambda item: image_order.get(
            str(item.get("image")).replace("\\", "/"),
            image_order.get(str(item.get("image")), len(image_order)),
        )
    )

    merged_payload: dict[str, Any] = {
        key: value
        for key, value in first_payload.items()
        if key
        not in {
            "time",
            "args",
            "upload_dir",
            "images",
            "results",
            "elapsed_seconds",
            "ok_count",
            "error_summary",
            "summary",
        }
    }
    merged_payload.update(
        {
            "time": datetime.now().isoformat(timespec="seconds"),
            "python": sys.executable,
            "model_path": args.model_path,
            "skills_dir": str(Path(args.skills_dir).expanduser()),
            "upload_dir": str(upload_dir),
            "args": vars(args),
            "parallel": {
                "mode": "data_parallel_shards",
                "gpu_ids": [worker["gpu_id"] for worker in workers],
                "worker_count": len(workers),
                "parallel_dir": str(parallel_dir),
                "workers": [
                    {
                        "worker_id": worker["worker_id"],
                        "gpu_id": worker["gpu_id"],
                        "image_count": worker["image_count"],
                        "return_code": worker.get("return_code"),
                        "output_dir": worker["output_dir"],
                        "log_path": worker["log_path"],
                        "latest_json": worker.get("latest_json"),
                    }
                    for worker in workers
                ],
            },
            "images": [str(image_path) for image_path in images],
            "results": results,
        }
    )
    merged_payload["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    merged_payload["ok_count"] = sum(1 for item in results if item.get("ok"))
    merged_payload["error_summary"] = summarize_error_metrics(results)
    merged_payload["summary"] = (
        f"OK images={merged_payload['ok_count']}/{len(images)}; "
        f"elapsed={merged_payload['elapsed_seconds']}s; "
        f"workers={len(workers)}; skills={len(merged_payload.get('skill_registry', []))}"
    )
    return merged_payload


def merge_diagnostic_worker_payloads(
    *,
    args: argparse.Namespace,
    images: list[Path],
    upload_dir: Path,
    worker_payloads: list[tuple[dict[str, Any], dict[str, Any]]],
    workers: list[dict[str, Any]],
    started: float,
    parallel_dir: Path,
) -> dict[str, Any]:
    first_payload = worker_payloads[0][1]
    image_order = {
        key: index
        for index, image_path in enumerate(images)
        for key in image_order_keys(image_path)
    }
    skill_order = {
        skill_id: index
        for index, skill_id in enumerate(first_payload.get("diagnostic_skills") or [])
    }
    results: list[dict[str, Any]] = []
    for worker, payload in worker_payloads:
        for item in payload.get("results", []):
            merged_item = dict(item)
            merged_item["worker_id"] = worker["worker_id"]
            merged_item["gpu_id"] = worker["gpu_id"]
            results.append(merged_item)
    results.sort(
        key=lambda item: (
            image_order.get(
                str(item.get("image")).replace("\\", "/"),
                image_order.get(str(item.get("image")), len(image_order)),
            ),
            skill_order.get(str(item.get("skill_id")), len(skill_order)),
        )
    )

    merged_payload: dict[str, Any] = {
        key: value
        for key, value in first_payload.items()
        if key
        not in {
            "time",
            "args",
            "upload_dir",
            "images",
            "results",
            "elapsed_seconds",
            "ok_count",
            "diagnostic_summary",
            "summary",
        }
    }
    merged_payload.update(
        {
            "time": datetime.now().isoformat(timespec="seconds"),
            "python": sys.executable,
            "model_path": args.model_path,
            "skills_dir": str(Path(args.skills_dir).expanduser()),
            "upload_dir": str(upload_dir),
            "args": vars(args),
            "parallel": {
                "mode": "diagnostic_data_parallel_shards",
                "gpu_ids": [worker["gpu_id"] for worker in workers],
                "worker_count": len(workers),
                "parallel_dir": str(parallel_dir),
                "workers": [
                    {
                        "worker_id": worker["worker_id"],
                        "gpu_id": worker["gpu_id"],
                        "image_count": worker["image_count"],
                        "return_code": worker.get("return_code"),
                        "output_dir": worker["output_dir"],
                        "log_path": worker["log_path"],
                        "latest_json": worker.get("latest_json"),
                    }
                    for worker in workers
                ],
            },
            "images": [str(image_path) for image_path in images],
            "results": results,
        }
    )
    merged_payload["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    merged_payload["ok_count"] = sum(1 for item in results if item.get("ok"))
    merged_payload["diagnostic_summary"] = summarize_diagnostic_results(results)
    merged_payload["summary"] = (
        f"Diagnostic OK calls={merged_payload['ok_count']}/{len(results)}; "
        f"images={len(images)}; elapsed={merged_payload['elapsed_seconds']}s; "
        f"workers={len(workers)}"
    )
    return merged_payload


def run_skill_diagnostic(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    project_root = Path(args.project_root).expanduser()
    upload_dir = resolve_upload_dir(args)
    base_output_dir = Path(args.output_dir).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    images = resolve_experiment_images(args, upload_dir)
    if not images:
        raise FileNotFoundError(f"No images found in {upload_dir}")
    output_dir = (
        base_output_dir
        if args.parallel_worker
        else run_output_dir(
            base_output_dir,
            args=args,
            upload_dir=upload_dir,
            images=images,
            worker_count=args.worker_count or 1,
        )
    )

    skill_specs = load_skill_specs_from_directory(
        skills_dir,
        include_duplicate_frontmatter_names=args.include_duplicate_skills,
    )
    skill_map = {spec.skill_id: spec for spec in skill_specs}
    diagnostic_skill_ids = args.diagnostic_skill or list(DEFAULT_DIAGNOSTIC_SKILLS)
    missing_skills = [skill_id for skill_id in diagnostic_skill_ids if skill_id not in skill_map]
    if missing_skills:
        raise ValueError(f"Diagnostic skill(s) not found: {', '.join(missing_skills)}")
    diagnostic_specs = [skill_map[skill_id] for skill_id in diagnostic_skill_ids]

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
        "args": vars(args),
        "diagnostic_skills": diagnostic_skill_ids,
        "images": [str(path) for path in images],
        "results": [],
    }

    print(f"Diagnostic images: {len(images)}")
    print(f"Diagnostic skills: {', '.join(diagnostic_skill_ids)}")
    print(f"Project root: {project_root}")
    print(f"Upload dir:   {upload_dir}")
    print(f"Output dir:   {output_dir}")

    for image_index, image_path in enumerate(images, start=1):
        image_input = ImageInput(image_path=str(image_path))
        print(f"[{image_index}/{len(images)}] {image_path}")
        for skill_spec in diagnostic_specs:
            item: dict[str, Any] = {
                "image": str(image_path),
                "skill_id": skill_spec.skill_id,
                "ok": False,
            }
            if args.worker_id is not None:
                item["worker_id"] = args.worker_id
            try:
                started_call = time.perf_counter()
                raw_payload = client.complete_json(
                    system_prompt=build_analysis_system_prompt(skill_spec),
                    user_prompt=build_analysis_user_prompt(
                        skill_id=skill_spec.skill_id,
                        route_reason="Diagnostic forced skill output schema check.",
                        user_context=args.user_context,
                    ),
                    image_payload=image_input.to_llm_payload(),
                )
                item["seconds"] = round(time.perf_counter() - started_call, 3)
                item["raw_model_text"] = getattr(client, "last_raw_output_text", "")
                item["raw_model_payload"] = raw_payload
                item["payload_keys"] = list(raw_payload.keys()) if isinstance(raw_payload, dict) else []
                item["classification"] = classify_skill_payload(raw_payload, skill_spec)

                try:
                    normalized = pipeline._normalize_analysis_result(skill_spec, raw_payload)
                    item["ok"] = True
                    item["normalized_va"] = {
                        "valence_score": normalized.valence_score,
                        "arousal_score": normalized.arousal_score,
                        "valence": normalized.valence,
                        "arousal": normalized.arousal,
                    }
                    recovery = normalized.raw_model_output.get("_parse_recovery")
                    if recovery:
                        item["parse_recovered"] = recovery
                    print(
                        f"  {skill_spec.skill_id}: ok "
                        f"Vscore={normalized.valence_score:.2f} "
                        f"Ascore={normalized.arousal_score:.2f} "
                        f"class={item['classification']}"
                    )
                except Exception as exc:
                    item["normalization_error_type"] = type(exc).__name__
                    item["normalization_error"] = str(exc)
                    item["normalization_traceback"] = traceback.format_exc()
                    print(
                        f"  {skill_spec.skill_id}: schema_error "
                        f"class={item['classification']} error={type(exc).__name__}: {exc}"
                    )
            except ModelOutputParseError as exc:
                item["classification"] = "invalid_json"
                item["error_type"] = type(exc).__name__
                item["error"] = str(exc)
                item["raw_model_text"] = exc.raw_text
                item["traceback"] = traceback.format_exc()
                print(f"  {skill_spec.skill_id}: parse_error {exc}")
            except Exception as exc:
                item["classification"] = "call_error"
                item["error_type"] = type(exc).__name__
                item["error"] = str(exc)
                item["raw_model_text"] = getattr(client, "last_raw_output_text", "")
                item["traceback"] = traceback.format_exc()
                print(f"  {skill_spec.skill_id}: call_error {type(exc).__name__}: {exc}")

            payload["results"].append(item)

    payload["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    payload["ok_count"] = sum(1 for item in payload["results"] if item.get("ok"))
    payload["diagnostic_summary"] = summarize_diagnostic_results(payload["results"])
    payload["summary"] = (
        f"Diagnostic OK calls={payload['ok_count']}/{len(payload['results'])}; "
        f"images={len(images)}; elapsed={payload['elapsed_seconds']}s"
    )
    mode = run_mode_slug(args)
    if not args.parallel_worker:
        attach_output_paths(payload, base_output_dir, output_dir, mode=mode)
    json_path, latest_json = write_diagnostic_outputs(output_dir, payload)
    if not args.parallel_worker:
        latest_dir = update_latest_outputs(base_output_dir, output_dir, mode=mode)
        print(f"Latest dir: {latest_dir}")
    print(payload["summary"])
    print(f"Saved: {json_path}")
    print(f"Latest: {latest_json}")
    return 0


def classify_skill_payload(payload: Any, skill_spec: Any) -> str:
    if not isinstance(payload, dict):
        return "non_object_payload"
    if not payload:
        return "empty_json_object"
    if payload.get("_parse_recovery") == "partial_json_scores":
        return "partial_json_scores"
    if {"valence_score", "arousal_score"}.issubset(payload.keys()):
        return "top_level_scores"
    if looks_like_emotion_weight_map(payload, skill_spec):
        return "emotion_weight_map_only"
    if has_score_aliases(payload):
        return "alias_or_nested_scores"
    text = payload_text(payload).upper()
    if "FINAL VALENCE" in text or "FINAL AROUSAL" in text or "VA TENDENCY" in text:
        return "skill_text_template"
    return "missing_score_fields"


def looks_like_emotion_weight_map(payload: dict[str, Any], skill_spec: Any) -> bool:
    emotion_terms = {str(item).lower() for item in getattr(skill_spec, "discrete_emotions", [])}
    if not emotion_terms:
        return False
    keys = {str(key).lower() for key in payload.keys()}
    if not keys or not keys.issubset(emotion_terms):
        return False
    return all(isinstance(value, (int, float)) for value in payload.values())


def has_score_aliases(payload: dict[str, Any]) -> bool:
    score_keys = {
        "valencescore",
        "arousalscore",
        "valence",
        "arousal",
        "finalvalence",
        "finalarousal",
        "finalva",
        "scores",
        "vascores",
        "va",
        "analysis",
        "output",
        "result",
    }

    def normalize_key(key: str) -> str:
        return "".join(ch for ch in key.lower() if ch.isalnum())

    def visit(value: Any) -> bool:
        if not isinstance(value, dict):
            return False
        for key, nested in value.items():
            if normalize_key(str(key)) in score_keys:
                return True
            if isinstance(nested, dict) and visit(nested):
                return True
        return False

    return visit(payload)


def payload_text(value: Any) -> str:
    chunks: list[str] = []

    def visit(item: Any) -> None:
        if isinstance(item, str):
            chunks.append(item)
        elif isinstance(item, dict):
            for nested in item.values():
                visit(nested)
        elif isinstance(item, list):
            for nested in item:
                visit(nested)

    visit(value)
    return "\n".join(chunks)


def summarize_diagnostic_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "total": len(results),
        "ok": sum(1 for item in results if item.get("ok")),
        "by_skill": {},
        "by_classification": {},
    }
    for item in results:
        skill_id = str(item.get("skill_id") or "<missing>")
        classification = str(item.get("classification") or "<missing>")
        skill_row = summary["by_skill"].setdefault(skill_id, {"total": 0, "ok": 0, "classifications": {}})
        skill_row["total"] += 1
        if item.get("ok"):
            skill_row["ok"] += 1
        skill_row["classifications"][classification] = skill_row["classifications"].get(classification, 0) + 1
        summary["by_classification"][classification] = summary["by_classification"].get(classification, 0) + 1
    return summary


def direct_baseline_spec() -> PsychologySkillSpec:
    return PsychologySkillSpec(
        skill_id="direct-va-baseline",
        display_name="Direct VA Baseline",
        short_description="Direct valence-arousal baseline without named psychology skill routing.",
        theory_family="direct-va",
        selection_hints=[],
        use_when="Use as a baseline for comparison against skill-routed VA analysis.",
        image_signals=[],
        va_focus="Directly estimate valence and arousal from visible image cues.",
        analysis_steps=[],
    )


def traced_complete_json(
    *,
    client: Qwen3VLClient,
    trace: list[dict[str, Any]],
    step: str,
    system_prompt: str,
    user_prompt: str,
    image_input: ImageInput,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "step": step,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "image_payload": image_input.to_llm_payload(),
        "system_prompt_chars": len(system_prompt),
        "user_prompt_chars": len(user_prompt),
        "max_new_tokens": getattr(client, "max_new_tokens", None),
    }
    if extra:
        entry.update(extra)

    started = time.perf_counter()
    try:
        payload = client.complete_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_payload=image_input.to_llm_payload(),
        )
        entry["seconds"] = round(time.perf_counter() - started, 3)
        entry["ok"] = True
        entry["raw_model_text"] = getattr(client, "last_raw_output_text", "")
        entry["raw_model_payload"] = payload
        entry["payload_keys"] = list(payload.keys()) if isinstance(payload, dict) else []
        entry["prompt_chars"] = len(getattr(client, "last_prompt_text", "") or "")
        entry["input_tokens"] = getattr(client, "last_input_token_count", None)
        entry["generated_tokens"] = getattr(client, "last_generated_token_count", None)
        entry["generation_hit_limit"] = getattr(client, "last_generation_hit_limit", False)
        trace.append(entry)
        return payload
    except ModelOutputParseError as exc:
        entry["seconds"] = round(time.perf_counter() - started, 3)
        entry["ok"] = False
        entry["error_type"] = type(exc).__name__
        entry["error"] = str(exc)
        entry["raw_model_text"] = exc.raw_text
        entry["prompt_chars"] = len(getattr(client, "last_prompt_text", "") or "")
        entry["input_tokens"] = getattr(client, "last_input_token_count", None)
        entry["generated_tokens"] = getattr(client, "last_generated_token_count", None)
        entry["generation_hit_limit"] = getattr(client, "last_generation_hit_limit", False)
        trace.append(entry)
        raise
    except Exception as exc:
        entry["seconds"] = round(time.perf_counter() - started, 3)
        entry["ok"] = False
        entry["error_type"] = type(exc).__name__
        entry["error"] = str(exc)
        entry["raw_model_text"] = getattr(client, "last_raw_output_text", "")
        entry["prompt_chars"] = len(getattr(client, "last_prompt_text", "") or "")
        entry["input_tokens"] = getattr(client, "last_input_token_count", None)
        entry["generated_tokens"] = getattr(client, "last_generated_token_count", None)
        entry["generation_hit_limit"] = getattr(client, "last_generation_hit_limit", False)
        trace.append(entry)
        raise


def candidate_skill_ids_for_route(route: RouteDecision, args: argparse.Namespace) -> list[str]:
    if route.skill_id == NO_SPECIALIZED_SKILL_ID:
        return []

    limit = args.max_candidate_skills if args.multi_skill_candidates else 1
    raw_skill_ids = list(getattr(route, "candidate_skill_ids", []) or [])
    if not raw_skill_ids:
        raw_skill_ids = [route.skill_id, *route.alternative_skill_ids]

    deduped: list[str] = []
    seen: set[str] = set()
    for skill_id in raw_skill_ids:
        if not skill_id or skill_id in seen:
            continue
        deduped.append(skill_id)
        seen.add(skill_id)
    if route.skill_id not in seen:
        deduped.insert(0, route.skill_id)
    return deduped[:limit]


def no_specialized_skill_selection(
    route: RouteDecision,
    direct_result: Any,
) -> dict[str, Any]:
    return {
        "selected_skill_id": NO_SPECIALIZED_SKILL_ID,
        "reason": route.reason or "No specialized skill strongly matched; using direct VA baseline.",
        "confidence": route.confidence,
        "selected_valence_score": getattr(direct_result, "valence_score", None),
        "selected_arousal_score": getattr(direct_result, "arousal_score", None),
        "rejected_candidates": [],
        "fallback": False,
        "used_direct_va": True,
    }


def direct_gate_fallback_selection(
    direct_result: Any,
    candidate_analyses: list[dict[str, Any]],
) -> dict[str, Any]:
    rejected = []
    for candidate in candidate_analyses:
        reasons = candidate.get("selection_gate_reasons") or []
        rejected.append(
            {
                "skill_id": candidate.get("skill_id"),
                "why_not": "; ".join(str(reason) for reason in reasons)
                or str(candidate.get("error") or "candidate analysis was not eligible"),
            }
        )
    return {
        "selected_skill_id": "direct-va-baseline",
        "reason": "All specialized candidates failed their evidence gate; retaining Direct VA.",
        "confidence": 1.0,
        "selected_valence_score": getattr(direct_result, "valence_score", None),
        "selected_arousal_score": getattr(direct_result, "arousal_score", None),
        "rejected_candidates": rejected,
        "fallback": True,
        "used_direct_va": True,
    }


def _score_extremity(score: Any) -> float | None:
    try:
        return abs(float(score) - 5.0)
    except (TypeError, ValueError):
        return None


def candidate_selection_gate_reasons(
    candidate: dict[str, Any],
    direct_result: Any | None,
) -> list[str]:
    if candidate.get("skill_id") != "facial-expression-affect":
        return []

    skill_va = candidate.get("skill_va") or {}
    raw = skill_va.get("raw_model_output") or {}
    reasons: list[str] = []
    if str(raw.get("applicability") or "").strip().lower() != "strong":
        reasons.append("facial-expression applicability is not strong")

    reliability = raw.get("face_reliability") or {}
    if reliability.get("face_clear") is not True:
        reasons.append("face is not reliably clear")
    if reliability.get("brow_eye_visible") is not True:
        reasons.append("brow/eye evidence is not reliable")
    if reliability.get("mouth_jaw_visible") is not True:
        reasons.append("mouth/jaw evidence is not reliable")
    if reliability.get("external_distortion") is not False:
        reasons.append("a hand/object distorts or occludes the face")

    if str(raw.get("gate_decision") or "").strip().lower() != "use_skill":
        reasons.append("model gate_decision did not approve skill use")
    viewer_transfer = raw.get("viewer_transfer") or {}
    if str(viewer_transfer.get("level") or "").strip().lower() not in {
        "low",
        "medium",
        "high",
    }:
        reasons.append("viewer-transfer estimate is missing")

    if direct_result is not None:
        for dimension in ("valence", "arousal"):
            skill_extremity = _score_extremity(skill_va.get(f"{dimension}_score"))
            direct_extremity = _score_extremity(getattr(direct_result, f"{dimension}_score", None))
            if (
                skill_extremity is not None
                and direct_extremity is not None
                and skill_extremity > direct_extremity + 1e-9
            ):
                reasons.append(
                    f"face-only analysis amplifies {dimension} beyond Direct instead of attenuating it"
                )
    return reasons


def eligible_candidate_analyses(
    candidate_analyses: list[dict[str, Any]],
    direct_result: Any | None,
) -> list[dict[str, Any]]:
    eligible: list[dict[str, Any]] = []
    for candidate in candidate_analyses:
        if not candidate.get("ok") or not candidate.get("skill_va"):
            candidate["selection_eligible"] = False
            candidate.setdefault("selection_gate_reasons", ["candidate analysis failed"])
            continue
        reasons = candidate_selection_gate_reasons(candidate, direct_result)
        candidate["selection_eligible"] = not reasons
        candidate["selection_gate_reasons"] = reasons
        if not reasons:
            eligible.append(candidate)
    return eligible


def analysis_prompts_for_skill(
    *,
    args: argparse.Namespace,
    selected_skill: PsychologySkillSpec,
    route: RouteDecision,
) -> tuple[str, str]:
    analysis_system_prompt = (
        build_full_skill_analysis_system_prompt(selected_skill)
        if args.full_skill_analysis
        else build_analysis_system_prompt(selected_skill)
    )
    analysis_user_prompt = build_analysis_user_prompt(
        skill_id=selected_skill.skill_id,
        route_reason=route.reason,
        user_context=args.user_context,
    )
    return analysis_system_prompt, analysis_user_prompt


def compact_candidate_for_selection(candidate: dict[str, Any]) -> dict[str, Any]:
    skill_va = candidate.get("skill_va") or {}
    raw_output = skill_va.get("raw_model_output") or {}
    return {
        "skill_id": candidate.get("skill_id"),
        "ok": candidate.get("ok"),
        "valence_score": skill_va.get("valence_score"),
        "arousal_score": skill_va.get("arousal_score"),
        "valence": skill_va.get("valence"),
        "arousal": skill_va.get("arousal"),
        "quadrant": skill_va.get("quadrant"),
        "summary": raw_output.get("summary") or skill_va.get("summary"),
        "applicability": raw_output.get("applicability"),
        "visual_evidence": raw_output.get("visual_evidence"),
        "evidence": raw_output.get("evidence") or skill_va.get("evidence"),
        "construct_estimates": raw_output.get("construct_estimates"),
        "skill_procedure_trace": raw_output.get("skill_procedure_trace"),
        "context_modifiers": raw_output.get("context_modifiers"),
        "va_judgment": raw_output.get("va_judgment"),
        "inference_summary": raw_output.get("inference_summary"),
        "uncertainty": raw_output.get("uncertainty") or skill_va.get("uncertainty"),
    }


def successful_candidate_analyses(candidate_analyses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [candidate for candidate in candidate_analyses if candidate.get("ok") and candidate.get("skill_va")]


def selected_candidate_for_selection(
    candidate_analyses: list[dict[str, Any]],
    selection: dict[str, Any],
) -> dict[str, Any]:
    selected_skill_id = selection.get("selected_skill_id")
    for candidate in candidate_analyses:
        if candidate.get("ok") and candidate.get("skill_id") == selected_skill_id:
            return candidate
    for candidate in candidate_analyses:
        if candidate.get("ok"):
            return candidate
    raise ValueError("No successful candidate skill analysis is available.")


def normalize_skill_selection_payload(
    payload: dict[str, Any],
    successful_candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    allowed = {str(candidate["skill_id"]): candidate for candidate in successful_candidates}
    selected_skill_id = str(
        payload.get("selected_skill_id")
        or payload.get("skill_id")
        or payload.get("selected_skill")
        or ""
    ).strip()
    fallback = False
    if selected_skill_id not in allowed:
        selected_skill_id = str(successful_candidates[0]["skill_id"])
        fallback = True

    selected_candidate = allowed[selected_skill_id]
    selected_va = selected_candidate.get("skill_va") or {}
    confidence = payload.get("confidence", 0.5)
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    return {
        "selected_skill_id": selected_skill_id,
        "reason": str(payload.get("reason") or "Selected the first valid candidate analysis."),
        "confidence": confidence,
        "selected_valence_score": selected_va.get("valence_score"),
        "selected_arousal_score": selected_va.get("arousal_score"),
        "selector_valence_score": payload.get("selected_valence_score"),
        "selector_arousal_score": payload.get("selected_arousal_score"),
        "rejected_candidates": payload.get("rejected_candidates") or [],
        "fallback": fallback,
        "raw_model_payload": payload,
    }


def fallback_skill_selection(
    successful_candidates: list[dict[str, Any]],
    *,
    reason: str,
    error: Exception | None = None,
) -> dict[str, Any]:
    selected = successful_candidates[0]
    selected_va = selected.get("skill_va") or {}
    selection = {
        "selected_skill_id": selected.get("skill_id"),
        "reason": reason,
        "confidence": 0.0,
        "selected_valence_score": selected_va.get("valence_score"),
        "selected_arousal_score": selected_va.get("arousal_score"),
        "rejected_candidates": [],
        "fallback": True,
    }
    if error is not None:
        selection["error_type"] = type(error).__name__
        selection["error"] = str(error)
    return selection


def select_final_skill_analysis(
    *,
    args: argparse.Namespace,
    client: Qwen3VLClient,
    image_input: ImageInput,
    route: RouteDecision,
    candidate_analyses: list[dict[str, Any]],
    trace: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    successful = successful_candidate_analyses(candidate_analyses)
    if not successful:
        raise ValueError("No candidate skill analysis succeeded.")
    if len(successful) == 1:
        return fallback_skill_selection(
            successful,
            reason="Only one candidate skill analysis succeeded; using it as the final score.",
        )

    candidate_skill_ids = [str(candidate["skill_id"]) for candidate in successful]
    system_prompt = build_skill_selection_system_prompt(candidate_skill_ids)
    user_prompt = build_skill_selection_user_prompt(
        route=route.to_dict(),
        candidate_analyses=[compact_candidate_for_selection(candidate) for candidate in successful],
        user_context=args.user_context,
    )
    try:
        if trace is not None:
            payload = traced_complete_json(
                client=client,
                trace=trace,
                step="skill_final_selection",
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                image_input=image_input,
                extra={"candidate_skill_ids": candidate_skill_ids},
            )
            selection = normalize_skill_selection_payload(payload, successful)
            trace[-1]["normalized_result"] = selection
            return selection

        payload, _seconds = timed_call(
            client.complete_json,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            image_payload=image_input.to_llm_payload(),
        )
        return normalize_skill_selection_payload(payload, successful)
    except Exception as exc:
        return fallback_skill_selection(
            successful,
            reason="Final skill selector failed; using the first successful routed candidate.",
            error=exc,
        )


def process_image_with_trace(
    *,
    args: argparse.Namespace,
    client: Qwen3VLClient,
    pipeline: PsychologyVAPipeline,
    skill_specs: list[Any],
    image_path: Path,
    index: int,
    total: int,
    annotations: dict[str, dict[str, float]],
) -> dict[str, Any]:
    print(f"[{index}/{total}] {image_path}")
    item: dict[str, Any] = {
        "image": str(image_path),
        "ok": False,
        "trace_inference": True,
        "inference_trace": [],
    }
    if args.worker_id is not None:
        item["worker_id"] = args.worker_id
    true_va = annotations.get(image_path.name)
    if true_va:
        item["true_va"] = true_va
    image_input = ImageInput(image_path=str(image_path))

    try:
        direct_result = None
        if not args.routed_only:
            direct_system_prompt = (
                build_full_direct_va_system_prompt()
                if args.full_skill_analysis
                else build_direct_va_system_prompt()
            )
            direct_user_prompt = build_direct_va_user_prompt(args.user_context)
            direct_payload = traced_complete_json(
                client=client,
                trace=item["inference_trace"],
                step="direct_va_baseline",
                system_prompt=direct_system_prompt,
                user_prompt=direct_user_prompt,
                image_input=image_input,
            )
            direct_result = pipeline._normalize_analysis_result(direct_baseline_spec(), direct_payload)
            direct_trace = item["inference_trace"][-1]
            direct_trace["normalized_result"] = direct_result.to_dict()
            item["direct_seconds"] = direct_trace["seconds"]
            item["direct_va"] = direct_result.to_dict()
            if true_va:
                item["direct_error"] = va_error(direct_result.to_dict(), true_va)
            print(
                f"  direct: Vscore={direct_result.valence_score:.2f} "
                f"Ascore={direct_result.arousal_score:.2f} "
                f"(norm V={direct_result.valence:.3f} A={direct_result.arousal:.3f}) "
                f"in {direct_trace['seconds']:.3f}s"
            )

        if not args.direct_only:
            routing_system_prompt = (
                build_full_routing_system_prompt(skill_specs)
                if args.full_skill_analysis
                else build_routing_system_prompt(skill_specs)
            )
            routing_user_prompt = build_routing_user_prompt(args.user_context)
            route_payload = traced_complete_json(
                client=client,
                trace=item["inference_trace"],
                step="route_skill",
                system_prompt=routing_system_prompt,
                user_prompt=routing_user_prompt,
                image_input=image_input,
            )
            route = pipeline._normalize_route_decision(route_payload, user_context=args.user_context)
            route_trace = item["inference_trace"][-1]
            route_trace["normalized_result"] = route.to_dict()
            item["route_seconds"] = route_trace["seconds"]
            item["route"] = route.to_dict()
            print(f"  route: {route.skill_id} conf={route.confidence:.2f} in {route_trace['seconds']:.3f}s")

            if route.skill_id == NO_SPECIALIZED_SKILL_ID:
                if direct_result is None:
                    direct_system_prompt = (
                        build_full_direct_va_system_prompt()
                        if args.full_skill_analysis
                        else build_direct_va_system_prompt()
                    )
                    direct_user_prompt = build_direct_va_user_prompt(args.user_context)
                    direct_payload = traced_complete_json(
                        client=client,
                        trace=item["inference_trace"],
                        step="direct_va_baseline_for_no_specialized_skill",
                        system_prompt=direct_system_prompt,
                        user_prompt=direct_user_prompt,
                        image_input=image_input,
                    )
                    direct_result = pipeline._normalize_analysis_result(direct_baseline_spec(), direct_payload)
                    direct_trace = item["inference_trace"][-1]
                    direct_trace["normalized_result"] = direct_result.to_dict()
                    item["direct_seconds"] = direct_trace["seconds"]
                    item["direct_va"] = direct_result.to_dict()
                    if true_va:
                        item["direct_error"] = va_error(direct_result.to_dict(), true_va)

                item["candidate_skill_ids"] = []
                item["candidate_skill_analyses"] = []
                selection = no_specialized_skill_selection(route, direct_result)
                item["skill_selection"] = selection
                item["skill_seconds"] = 0.0
                item["total_candidate_skill_seconds"] = 0.0
                item["skill_va"] = direct_result.to_dict()
                if true_va:
                    item["skill_error"] = va_error(item["skill_va"], true_va)
                item["delta"] = delta(item["skill_va"], direct_result.to_dict())
                print(
                    f"  selected: {NO_SPECIALIZED_SKILL_ID} "
                    f"Vscore={item['skill_va'].get('valence_score'):.2f} "
                    f"Ascore={item['skill_va'].get('arousal_score'):.2f} "
                    "using direct VA baseline"
                )
                item["ok"] = True
                return item

            candidate_skill_ids = candidate_skill_ids_for_route(route, args)
            item["candidate_skill_ids"] = candidate_skill_ids
            item["candidate_skill_analyses"] = []
            print(f"  candidates: {', '.join(candidate_skill_ids)}")

            for candidate_index, candidate_skill_id in enumerate(candidate_skill_ids, start=1):
                selected_skill = pipeline.skill_map[candidate_skill_id]
                analysis_system_prompt, analysis_user_prompt = analysis_prompts_for_skill(
                    args=args,
                    selected_skill=selected_skill,
                    route=route,
                )
                candidate_item: dict[str, Any] = {
                    "skill_id": candidate_skill_id,
                    "candidate_index": candidate_index,
                    "ok": False,
                }
                step_name = "skill_analysis" if len(candidate_skill_ids) == 1 else "candidate_skill_analysis"
                try:
                    skill_payload = traced_complete_json(
                        client=client,
                        trace=item["inference_trace"],
                        step=step_name,
                        system_prompt=analysis_system_prompt,
                        user_prompt=analysis_user_prompt,
                        image_input=image_input,
                        extra={
                            "skill_id": candidate_skill_id,
                            "candidate_index": candidate_index,
                            "route_reason": route.reason,
                        },
                    )
                    skill_result = pipeline._normalize_analysis_result(selected_skill, skill_payload)
                    skill_trace = item["inference_trace"][-1]
                    skill_trace["normalized_result"] = skill_result.to_dict()
                    candidate_item.update(
                        {
                            "ok": True,
                            "seconds": skill_trace["seconds"],
                            "skill_va": skill_result.to_dict(),
                            "trace_step": step_name,
                        }
                    )
                    raw_output = candidate_item["skill_va"].get("raw_model_output") or {}
                    if raw_output.get("_parse_recovery"):
                        candidate_item["parse_recovered"] = raw_output["_parse_recovery"]
                    print(
                        f"  candidate {candidate_index}/{len(candidate_skill_ids)} "
                        f"{candidate_skill_id}: Vscore={skill_result.valence_score:.2f} "
                        f"Ascore={skill_result.arousal_score:.2f} "
                        f"(norm V={skill_result.valence:.3f} A={skill_result.arousal:.3f}) "
                        f"in {skill_trace['seconds']:.3f}s"
                    )
                except Exception as exc:
                    candidate_item.update(
                        {
                            "ok": False,
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                            "traceback": traceback.format_exc(),
                            "raw_error_output": getattr(client, "last_raw_output_text", ""),
                        }
                    )
                    print(f"  candidate {candidate_skill_id}: ERROR {type(exc).__name__}: {exc}")
                item["candidate_skill_analyses"].append(candidate_item)

            item["total_candidate_skill_seconds"] = round(
                sum(float(candidate.get("seconds") or 0) for candidate in item["candidate_skill_analyses"]),
                3,
            )
            eligible_candidates = eligible_candidate_analyses(
                item["candidate_skill_analyses"], direct_result
            )
            if not eligible_candidates and direct_result is not None:
                selection = direct_gate_fallback_selection(
                    direct_result, item["candidate_skill_analyses"]
                )
                item["skill_selection"] = selection
                item["skill_seconds"] = 0.0
                item["skill_va"] = direct_result.to_dict()
            else:
                selection_pool = eligible_candidates or successful_candidate_analyses(
                    item["candidate_skill_analyses"]
                )
                selection = select_final_skill_analysis(
                    args=args,
                    client=client,
                    image_input=image_input,
                    route=route,
                    candidate_analyses=selection_pool,
                    trace=item["inference_trace"],
                )
                item["skill_selection"] = selection
                selected_candidate = selected_candidate_for_selection(
                    item["candidate_skill_analyses"], selection
                )
                item["skill_seconds"] = selected_candidate.get("seconds")
                item["skill_va"] = selected_candidate["skill_va"]
            if true_va:
                item["skill_error"] = va_error(item["skill_va"], true_va)
            raw_output = item["skill_va"].get("raw_model_output") or {}
            if raw_output.get("_parse_recovery"):
                item["parse_recovered"] = raw_output["_parse_recovery"]
                print(f"  parse: recovered from {raw_output['_parse_recovery']}")
            print(
                f"  selected: {selection.get('selected_skill_id')} "
                f"Vscore={item['skill_va'].get('valence_score'):.2f} "
                f"Ascore={item['skill_va'].get('arousal_score'):.2f} "
                f"reason={preview_text(str(selection.get('reason') or ''), limit=180)}"
            )
            if direct_result is not None:
                item["delta"] = delta(item["skill_va"], direct_result.to_dict())

        item["ok"] = True
    except Exception as exc:
        item["error_type"] = type(exc).__name__
        item["error"] = str(exc)
        if isinstance(exc, ModelOutputParseError):
            item["raw_error_output"] = exc.raw_text
        else:
            last_raw_output = getattr(client, "last_raw_output_text", "")
            if last_raw_output:
                item["raw_error_output"] = last_raw_output
        item["traceback"] = traceback.format_exc()
        print(f"  ERROR: {type(exc).__name__}: {exc}")

    return item


def run_single(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    project_root = Path(args.project_root).expanduser()
    upload_dir = resolve_upload_dir(args)
    base_output_dir = Path(args.output_dir).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    images = resolve_experiment_images(args, upload_dir)
    if not images:
        raise FileNotFoundError(f"No images found in {upload_dir}")
    output_dir = (
        base_output_dir
        if args.parallel_worker
        else run_output_dir(
            base_output_dir,
            args=args,
            upload_dir=upload_dir,
            images=images,
            worker_count=args.worker_count or 1,
        )
    )
    annotations_path = resolve_annotations_path(args, upload_dir)
    annotations = load_annotations(annotations_path)
    if args.parallel_worker:
        write_worker_progress(output_dir, completed=0, total=len(images))

    skill_specs = load_skill_specs_from_directory(
        skills_dir,
        include_duplicate_frontmatter_names=args.include_duplicate_skills,
    )
    if args.dry_run or args.list_skills:
        print_skill_registry(skill_specs)
        print(f"Project root: {project_root}")
        print(f"Skills dir:   {skills_dir}")
        print(f"Upload dir:   {upload_dir}")
        print(f"Output base:  {base_output_dir}")
        print(f"Output run:   {output_dir}")
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
            "raw_score_neutral": 5,
            "raw_score_max": 9,
            "normalization": "normalized = (score - 1) / 8",
            "valence_score": "1=very negative, 5=neutral, 9=very positive",
            "arousal_score": "1=very calm/deactivated, 5=moderate activation, 9=highly activated",
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
        "trace_inference": args.trace_inference,
        "full_skill_analysis": args.full_skill_analysis,
        "write_inference_markdown": args.write_inference_markdown,
        "iaps_trace_case_ids": collect_iaps_case_ids(args, upload_dir),
        "images": [str(path) for path in images],
        "results": [],
    }

    print_skill_registry(skill_specs)
    print(f"Images: {len(images)}")
    if annotations_path:
        print(f"Annotations: {annotations_path} ({len(annotations)})")

    for index, image_path in enumerate(images, start=1):
        if args.trace_inference:
            item = process_image_with_trace(
                args=args,
                client=client,
                pipeline=pipeline,
                skill_specs=skill_specs,
                image_path=image_path,
                index=index,
                total=len(images),
                annotations=annotations,
            )
            payload["results"].append(item)
            if args.parallel_worker:
                write_worker_progress(
                    output_dir,
                    completed=index,
                    total=len(images),
                    last_image=str(image_path),
                    last_ok=bool(item.get("ok")),
                )
            else:
                print(
                    format_progress_line(
                        completed=index,
                        total=len(images),
                        elapsed_seconds=time.perf_counter() - started,
                    )
                )
            continue

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

                if route.skill_id == NO_SPECIALIZED_SKILL_ID:
                    if direct_result is None:
                        direct_result, direct_seconds = timed_call(
                            pipeline.analyze_direct,
                            image_input=image_input,
                            user_context=args.user_context,
                        )
                        item["direct_seconds"] = round(direct_seconds, 3)
                        item["direct_va"] = direct_result.to_dict()
                        if true_va:
                            item["direct_error"] = va_error(direct_result.to_dict(), true_va)

                    item["candidate_skill_ids"] = []
                    item["candidate_skill_analyses"] = []
                    selection = no_specialized_skill_selection(route, direct_result)
                    item["skill_selection"] = selection
                    item["skill_seconds"] = 0.0
                    item["total_candidate_skill_seconds"] = 0.0
                    item["skill_va"] = direct_result.to_dict()
                    if true_va:
                        item["skill_error"] = va_error(item["skill_va"], true_va)
                    item["delta"] = delta(item["skill_va"], direct_result.to_dict())
                    print(
                        f"  selected: {NO_SPECIALIZED_SKILL_ID} "
                        f"Vscore={item['skill_va'].get('valence_score'):.2f} "
                        f"Ascore={item['skill_va'].get('arousal_score'):.2f} "
                        "using direct VA baseline"
                    )
                    item["ok"] = True
                    payload["results"].append(item)
                    if args.parallel_worker:
                        write_worker_progress(
                            output_dir,
                            completed=index,
                            total=len(images),
                            last_image=str(image_path),
                            last_ok=True,
                        )
                    else:
                        print(
                            format_progress_line(
                                completed=index,
                                total=len(images),
                                elapsed_seconds=time.perf_counter() - started,
                            )
                        )
                    continue

                candidate_skill_ids = candidate_skill_ids_for_route(route, args)
                item["candidate_skill_ids"] = candidate_skill_ids
                item["candidate_skill_analyses"] = []
                print(f"  candidates: {', '.join(candidate_skill_ids)}")

                for candidate_index, candidate_skill_id in enumerate(candidate_skill_ids, start=1):
                    candidate_route = RouteDecision(
                        skill_id=candidate_skill_id,
                        reason=route.reason,
                        confidence=route.confidence,
                        observed_cues=route.observed_cues,
                        alternative_skill_ids=route.alternative_skill_ids,
                        candidate_skill_ids=route.candidate_skill_ids,
                    )
                    candidate_item: dict[str, Any] = {
                        "skill_id": candidate_skill_id,
                        "candidate_index": candidate_index,
                        "ok": False,
                    }
                    try:
                        skill_result, skill_seconds = timed_call(
                            pipeline.analyze_with_route,
                            image_input=image_input,
                            route=candidate_route,
                            user_context=args.user_context,
                        )
                        candidate_item.update(
                            {
                                "ok": True,
                                "seconds": round(skill_seconds, 3),
                                "skill_va": skill_result.to_dict(),
                            }
                        )
                        print(
                            f"  candidate {candidate_index}/{len(candidate_skill_ids)} "
                            f"{candidate_skill_id}: Vscore={skill_result.valence_score:.2f} "
                            f"Ascore={skill_result.arousal_score:.2f} "
                            f"(norm V={skill_result.valence:.3f} A={skill_result.arousal:.3f}) "
                            f"in {skill_seconds:.3f}s"
                        )
                    except Exception as exc:
                        candidate_item.update(
                            {
                                "ok": False,
                                "error_type": type(exc).__name__,
                                "error": str(exc),
                                "traceback": traceback.format_exc(),
                                "raw_error_output": getattr(client, "last_raw_output_text", ""),
                            }
                        )
                        print(f"  candidate {candidate_skill_id}: ERROR {type(exc).__name__}: {exc}")
                    item["candidate_skill_analyses"].append(candidate_item)

                item["total_candidate_skill_seconds"] = round(
                    sum(float(candidate.get("seconds") or 0) for candidate in item["candidate_skill_analyses"]),
                    3,
                )
                eligible_candidates = eligible_candidate_analyses(
                    item["candidate_skill_analyses"], direct_result
                )
                if not eligible_candidates and direct_result is not None:
                    selection = direct_gate_fallback_selection(
                        direct_result, item["candidate_skill_analyses"]
                    )
                    item["skill_selection"] = selection
                    item["skill_seconds"] = 0.0
                    item["skill_va"] = direct_result.to_dict()
                else:
                    selection_pool = eligible_candidates or successful_candidate_analyses(
                        item["candidate_skill_analyses"]
                    )
                    selection = select_final_skill_analysis(
                        args=args,
                        client=client,
                        image_input=image_input,
                        route=route,
                        candidate_analyses=selection_pool,
                    )
                    item["skill_selection"] = selection
                    selected_candidate = selected_candidate_for_selection(
                        item["candidate_skill_analyses"], selection
                    )
                    item["skill_seconds"] = selected_candidate.get("seconds")
                    item["skill_va"] = selected_candidate["skill_va"]
                if true_va:
                    item["skill_error"] = va_error(item["skill_va"], true_va)
                raw_output = item["skill_va"].get("raw_model_output") or {}
                if raw_output.get("_parse_recovery"):
                    item["parse_recovered"] = raw_output["_parse_recovery"]
                    print(f"  parse: recovered from {raw_output['_parse_recovery']}")
                print(
                    f"  selected: {selection.get('selected_skill_id')} "
                    f"Vscore={item['skill_va'].get('valence_score'):.2f} "
                    f"Ascore={item['skill_va'].get('arousal_score'):.2f} "
                    f"reason={preview_text(str(selection.get('reason') or ''), limit=180)}"
                )
                if direct_result is not None:
                    item["delta"] = delta(item["skill_va"], direct_result.to_dict())

            item["ok"] = True
        except Exception as exc:
            item["error_type"] = type(exc).__name__
            item["error"] = str(exc)
            if isinstance(exc, ModelOutputParseError):
                item["raw_error_output"] = exc.raw_text
            else:
                last_raw_output = getattr(client, "last_raw_output_text", "")
                if last_raw_output:
                    item["raw_error_output"] = last_raw_output
            item["traceback"] = traceback.format_exc()
            print(f"  ERROR: {type(exc).__name__}: {exc}")

        payload["results"].append(item)
        if args.parallel_worker:
            write_worker_progress(
                output_dir,
                completed=index,
                total=len(images),
                last_image=str(image_path),
                last_ok=bool(item.get("ok")),
            )
        else:
            print(
                format_progress_line(
                    completed=index,
                    total=len(images),
                    elapsed_seconds=time.perf_counter() - started,
                )
            )

    payload["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    payload["ok_count"] = sum(1 for item in payload["results"] if item.get("ok"))
    payload["error_summary"] = summarize_error_metrics(payload["results"])
    payload["summary"] = (
        f"OK images={payload['ok_count']}/{len(images)}; "
        f"elapsed={payload['elapsed_seconds']}s; skills={len(skill_specs)}"
    )
    mode = run_mode_slug(args)
    if not args.parallel_worker:
        attach_output_paths(payload, base_output_dir, output_dir, mode=mode)
    json_path, latest_json = write_outputs(output_dir, payload)
    if args.trace_inference:
        trace_latest = write_trace_latest(output_dir, payload)
        print(f"Trace latest: {trace_latest}")
        if args.full_skill_analysis:
            full_skill_latest = write_full_skill_latest(output_dir, payload)
            print(f"Full-skill latest: {full_skill_latest}")
        if args.write_inference_markdown:
            md_path, latest_md = write_inference_markdown(output_dir, payload)
            print(f"Inference Markdown: {md_path}")
            print(f"Inference Markdown latest: {latest_md}")
    if not args.parallel_worker:
        latest_dir = update_latest_outputs(base_output_dir, output_dir, mode=mode)
        print(f"Latest dir: {latest_dir}")
    print(payload["summary"])
    print(f"Saved: {json_path}")
    print(f"Latest: {latest_json}")
    return 0 if payload["ok_count"] == len(images) else 1


def main() -> int:
    args = parse_args()
    if args.parallel_gpus and not args.parallel_worker and not args.dry_run and not args.list_skills:
        return run_parallel(args)
    if args.diagnose_skill_output and not args.dry_run and not args.list_skills:
        return run_skill_diagnostic(args)
    return run_single(args)


if __name__ == "__main__":
    raise SystemExit(main())
