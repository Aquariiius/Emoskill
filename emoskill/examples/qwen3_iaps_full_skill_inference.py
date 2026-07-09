from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from qwen3_skill_experiment import DEFAULT_IAPS_ALBUM_DIR, main


def _has_any(*flags: str) -> bool:
    return any(flag in sys.argv[1:] for flag in flags)


if __name__ == "__main__":
    injected_args: list[str] = []
    if not _has_any("--album-path", "--upload-dir"):
        injected_args.extend(["--album-path", DEFAULT_IAPS_ALBUM_DIR])
    if not _has_any("--full-skill-inference", "--full-skill-analysis"):
        injected_args.append("--full-skill-inference")
    if not _has_any("--four-gpu", "--parallel-gpus"):
        injected_args.append("--four-gpu")

    sys.argv[1:1] = injected_args
    raise SystemExit(main())
