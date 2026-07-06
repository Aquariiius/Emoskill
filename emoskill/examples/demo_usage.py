from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from psychology_va import ImageInput, PsychologyVAPipeline, Qwen3VLClient, load_skill_specs_from_directory


if __name__ == "__main__":
    client = Qwen3VLClient(
        model_name="/home/u1120250383/dyp/models/qwen",
        device_map="auto",
        max_new_tokens=512,
        max_pixels=1003520,
    )
    skill_specs = load_skill_specs_from_directory(PROJECT_ROOT / ".trae" / "skills")
    pipeline = PsychologyVAPipeline(llm_client=client, skill_specs=skill_specs)

    image_input = ImageInput(image_path="/home/u1120250383/dcs/Emoskill_test/uploads/haha.png")
    user_context = "Analyze the image's valence-arousal state and choose the best psychology skill."

    route = pipeline.route_skill(image_input=image_input, user_context=user_context)
    result = pipeline.analyze_with_route(
        image_input=image_input,
        route=route,
        user_context=user_context,
    )

    print(json.dumps({"route": route.to_dict(), "analysis": result.to_dict()}, ensure_ascii=False, indent=2))
