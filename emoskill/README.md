# Psychology VA Skeleton

This repository contains a psychology-guided visual affect analysis pipeline for local Qwen-VL models.

It is designed for the workflow:

1. summarize psychology models as reusable skills
2. send an image to a local `Qwen3-VL` model
3. let the LLM choose the best psychology model
4. run valence-arousal analysis with the selected model

## Included Skills

- `kaplan-art-restoration`
- `berlyne-arousal-pleasure`
- `awe`
- `cognitive-appraisal`
- `facial-expression-affect`
- `emotional-body-language`
- `evolved-fear-module`
- `pathogen-disgust`
- `baby-schema`

The active skill files are stored in `.trae/skills/`. `facial-expression-affect` handles clear transient expressions and viewer VA. `todorov-face-evaluation` remains available only for explicit non-VA social-impression analysis and is excluded from the main affect router.

## Code Layout

- `src/psychology_va/schemas.py`
  data structures for image input, routing, and final VA output
- `src/psychology_va/model_catalog.py`
  built-in psychology model registry
- `src/psychology_va/prompts.py`
  routing and analysis prompts for the multimodal LLM
- `src/psychology_va/llm_client.py`
  `Qwen25VLClient` for local/server-side `Qwen2.5-VL`
- `src/psychology_va/pipeline.py`
  two-stage pipeline: route skill -> analyze image
- `examples/demo_usage.py`
  example usage with `Qwen2.5-VL`

## Design Notes

- `Qwen3VLClient` loads the model through `transformers` and runs inference locally or on your own server.
- Image input supports `image_path`, `image_url`, and `image_b64`.
- The model is prompted to return JSON, and the client extracts the JSON object from the generation result.
- `StubMultimodalLLMClient` is kept only as a compatibility placeholder.
- Every active Skill v2 contains one applicability gate, observable visual variables, a numbered inference procedure, qualitative VA judgment, a worked example, and a compact output contract.
- All VA outputs use a shared 1-9 scale: valence 1/5/9 = negative/neutral/positive and arousal 1/5/9 = low/moderate/high activation.
- Per-skill hard VA lookup tables have been removed; scores must follow the visual inference procedure and shared scale.

## Server Dependencies

- `torch`
- `transformers`
- `Pillow`
- `requests`
- `accelerate` for easier multi-device loading
- `tqdm` for the optional four-GPU progress bar; a built-in text fallback is used when unavailable

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
