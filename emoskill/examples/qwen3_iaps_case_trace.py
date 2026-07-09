from __future__ import annotations

import sys

from qwen3_skill_experiment import DEFAULT_IAPS_ALBUM_DIR, main


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.extend(
            [
                "--album-path",
                DEFAULT_IAPS_ALBUM_DIR,
                "--iaps-trace-cases",
                "--trace-inference",
                "--four-gpu",
            ]
        )
    raise SystemExit(main())
