# Psychology VA Skeleton

This repository now contains a starter skeleton for psychology-guided visual affect analysis.
The current code path is designed for server-side deployment with `Qwen2.5-VL` instead of remote LLM APIs.

It is designed for the workflow:

1. summarize psychology models as reusable skills
2. send an image to a local `Qwen2.5-VL` model
3. let the LLM choose the best psychology model
4. run valence-arousal analysis with the selected model

## Included Skills

- `panas-discrete-va`
- `kaplan-art-restoration`
- `berlyne-arousal-pleasure`
- `todorov-face-evaluation`

The skill files are stored in `.trae/skills/`.

## Code Layout

- `src/psychology_va/schemas.py`
  data structures for image input, routing, and final VA output
- `src/psychology_va/model_catalog.py`
  built-in psychology model registry
- `src/psychology_va/mapping_tables.py`
  PANAS discrete emotion to VA mapping table
- `src/psychology_va/prompts.py`
  routing and analysis prompts for the multimodal LLM
- `src/psychology_va/llm_client.py`
  `Qwen25VLClient` for local/server-side `Qwen2.5-VL`
- `src/psychology_va/pipeline.py`
  two-stage pipeline: route skill -> analyze image
- `examples/demo_usage.py`
  example usage with `Qwen2.5-VL`

## Design Notes

- The default deployment target is `Qwen/Qwen2.5-VL-7B-Instruct`.
- `Qwen25VLClient` loads the model through `transformers` and runs inference locally or on your own server.
- Image input supports `image_path`, `image_url`, and `image_b64`.
- The model is prompted to return JSON, and the client extracts the JSON object from the generation result.
- `StubMultimodalLLMClient` is kept only as a compatibility placeholder.
- The default psychology model set is now centered on `PANAS`, `Kaplan ART`, `Berlyne`, and `Todorov face evaluation`.

## Server Dependencies

- `torch`
- `transformers`
- `Pillow`
- `requests`
- `accelerate` for easier multi-device loading

## Next Recommended Step

Deploy the code on a GPU server, install the dependencies above, then adjust `model_name`, `torch_dtype`, and `device_map` based on your hardware.

## Qwen3-VL Skill Routing Experiment

The current experiment version adds:

- `Qwen3VLClient` for local Qwen3-VL inference
- dynamic `.trae/skills/*/SKILL.md` loading
- direct VA baseline
- skill routing
- selected-skill VA analysis
- JSON and CSV experiment output

Run on the server after activating the working Qwen environment:

```bash
cd /home/u1120250383/dcs/Emoskill_test/emoskill
python examples/qwen3_skill_experiment.py
```

Default paths:

- model: `/home/u1120250383/dyp/models/qwen`
- images: `/home/u1120250383/dcs/Emoskill_test/uploads`
- skills: `./.trae/skills`
- output: `/home/u1120250383/dcs/Emoskill_test/script_output`

Outputs:

- `qwen3_skill_experiment_latest.json`
- `qwen3_skill_experiment_latest.csv`

Use one image only:

```bash
python examples/qwen3_skill_experiment.py --image /home/u1120250383/dcs/Emoskill_test/uploads/haha.png
```

Include duplicate frontmatter skill names if needed:

```bash
python examples/qwen3_skill_experiment.py --include-duplicate-skills
```
