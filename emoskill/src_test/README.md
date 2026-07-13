# Isolated VA-Mapping 9-Skill Experiment

This directory is a self-contained ablation architecture. It does not import or modify the main `src/psychology_va` package and does not use the main `.trae/skills` directory.

## Architecture

1. Direct VA baseline estimates Valence and Arousal on the shared 1-9 scale.
2. The router selects zero, one, or two candidates from the nine bundled skills.
3. Each selected skill follows its observable reasoning steps and produces a `skill_candidate` VA using its own `VA Mapping` table.
4. The fixed applicability weight is applied: Strong 0.85, Partial 0.55, or Weak 0.25.
5. Final VA is computed as `direct + weight * (skill_candidate - direct)` for each dimension.
6. The isolated validator rejects outputs that alter Direct VA, use the wrong weight, or violate the formula.
7. With no specialized match, Direct VA is retained. With two valid candidates, the existing final selector chooses one already-computed candidate; it does not average them.

## Directory Layout

- `qwen3_va_mapping_9skill_experiment.py`: isolated experiment entry point, four-GPU sharding, progress display, and result merging.
- `psychology_va/`: isolated loader, prompts, validation, schemas, and model client.
- `skills/`: the nine VA-mapping skills, including the restored English Todorov skill.

## Server Run

```bash
cd /home/u1120250383/dcs/Emoskill/emoskill

python src_test/qwen3_va_mapping_9skill_experiment.py \
  --model-path /home/u1120250383/dyp/models/qwen \
  --album-path /home/u1120250383/dcs/datasets/IAPS/Dataset \
  --output-dir /home/u1120250383/dcs/Emoskill/script_output/va_mapping_9skill_batch \
  --four-gpu \
  --multi-skill-candidates \
  --max-candidate-skills 2 \
  --max-new-tokens 2048
```
