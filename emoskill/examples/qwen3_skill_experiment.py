from __future__ import annotations

import argparse
import csv
import json
import math
import os
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
    PsychologyVAPipeline,
    Qwen3VLClient,
    load_skill_specs_from_directory,
)
from psychology_va.prompts import build_analysis_system_prompt, build_analysis_user_prompt


DEFAULT_MODEL_PATH = "/home/u1120250383/dyp/models/qwen"
DEFAULT_PROJECT_ROOT = "/home/u1120250383/dcs/Emoskill_test"
DEFAULT_OUTPUT_DIR = "/home/u1120250383/dcs/Emoskill/script_output"
DEFAULT_IAPS_ALBUM_DIR = "/home/u1120250383/dcs/datasets/IAPS/Dataset"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
REQUIRED_SKILL_SECTIONS = ("Purpose", "Output Format")
USE_WHEN_SECTION_NAMES = ("Use When", "Use-When Rules")
DEFAULT_DIAGNOSTIC_SKILLS = ("berlyne-arousal-pleasure", "panas-discrete-va")


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
            "Can be repeated. Defaults to berlyne-arousal-pleasure and panas-discrete-va."
        ),
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
                "worker_id": item.get("worker_id"),
                "gpu_id": item.get("gpu_id"),
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


def image_order_keys(image_path: Path) -> list[str]:
    raw = str(image_path)
    return [raw, raw.replace("\\", "/"), image_path.as_posix()]


def run_parallel(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    gpu_ids = parse_gpu_ids(args.parallel_gpus)
    project_root = Path(args.project_root).expanduser()
    upload_dir = resolve_upload_dir(args)
    output_dir = Path(args.output_dir).expanduser()
    images = find_images(upload_dir, args.image, args.image_list)
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
    parallel_dir = output_dir / f"qwen3_skill_experiment_parallel_{stamp}"
    parallel_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"Parallel run: images={len(images)}, workers={len(active_shards)}, "
        f"gpus={','.join(gpu_id for _, gpu_id, _ in active_shards)}"
    )
    print(f"Album: {upload_dir}")
    print(f"Parallel artifacts: {parallel_dir}")

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

    if args.diagnose_skill_output:
        json_path, latest_json = write_diagnostic_outputs(output_dir, merged_payload)
    else:
        json_path, latest_json = write_outputs(output_dir, merged_payload)
    print(merged_payload["summary"])
    print(f"Merged: {json_path}")
    print(f"Latest: {latest_json}")
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
    if args.diagnose_skill_output:
        command.append("--diagnose-skill-output")
        for skill_id in args.diagnostic_skill:
            command.extend(["--diagnostic-skill", str(skill_id)])
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
    output_dir = Path(args.output_dir).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    images = find_images(upload_dir, args.image, args.image_list)
    if not images:
        raise FileNotFoundError(f"No images found in {upload_dir}")

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
    json_path, latest_json = write_diagnostic_outputs(output_dir, payload)
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


def run_single(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    project_root = Path(args.project_root).expanduser()
    upload_dir = resolve_upload_dir(args)
    output_dir = Path(args.output_dir).expanduser()
    skills_dir = Path(args.skills_dir).expanduser()
    images = find_images(upload_dir, args.image, args.image_list)
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
            else:
                last_raw_output = getattr(client, "last_raw_output_text", "")
                if last_raw_output:
                    item["raw_error_output"] = last_raw_output
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


def main() -> int:
    args = parse_args()
    if args.parallel_gpus and not args.parallel_worker and not args.dry_run and not args.list_skills:
        return run_parallel(args)
    if args.diagnose_skill_output and not args.dry_run and not args.list_skills:
        return run_skill_diagnostic(args)
    return run_single(args)


if __name__ == "__main__":
    raise SystemExit(main())
