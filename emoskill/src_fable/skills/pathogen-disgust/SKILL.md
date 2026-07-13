---
name: "pathogen-disgust"
description: "Analyze pathogen avoidance from visible contamination, decay, waste, spoiled organic matter, wounds, fluids, parasites, or infestation. Infer extent, contact potential, realism, and medical/culinary/scientific/fictional attenuation before VA. Do not use for moral disgust, predator attack, abstract ugliness, or clean clinical content without pathogen cues."
---

# Pathogen Disgust

## Applicability Gate

REQUIRED:
- Visible organic contamination, decay, disease, waste, fluid, wound, spoiled food, parasite, or infestation is affectively central.
- Avoidance/rejection explains the response better than attack threat, sadness, or composition.
- Cue identity is visually supported, not inferred from a label or backstory.

REJECT:
- Moral or social violation without visible pathogen cues.
- Snake, predator, or attack morphology dominates.
- Fresh appetitive food, clean medical equipment, or harmless insects without contamination.

NEAR MISS:
- Predation or attack -> evolved-fear-module.
- Injury where human stakes dominate -> cognitive-appraisal; stay here only if contamination is central.
- Chaotic abstraction without organic contamination -> berlyne-arousal-pleasure or none.

## Visual Variables

- **Cue type**: rot, mold, decomposition, pus, vomit, feces, pooled blood, exposed tissue, spoiled food, parasites, infestation.
- **Extent/density**: localized trace versus widespread contamination or dense infestation.
- **Contact potential**: touch, ingestion relevance, proximity, leakage, containment.
- **Material state**: wetness, slime, oozing, discoloration, texture breakdown.
- **Context attenuation**: medical care, specimen, fermentation, packaging, fiction, barriers.

## Inference Procedure

1. Identify the visible pathogen cue; separate observation from uncertain identification.
2. Estimate extent, contact potential, and degradation from visible evidence.
3. Distinguish contamination from attack threat and from fresh treated injury.
4. Apply medical/culinary/scientific/fictional attenuation without erasing vivid cues.
5. Judge VA with the anchors. Disgust reliably LOWERS valence; it raises arousal much less.

## Arousal Gate

Disgust is an avoidance response, not an alarm response: most contamination sits at 4-5.2
arousal. Raise arousal above 5.5 only for imminent contact, fresh gore/exposed tissue, or
uncontrolled spread toward the viewer. Static rot, mess, or stains are NOT activation cues.
No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| Severe bodily gore: mutilation, exposed tissue, fresh wounds | 1.5-2.5 | 5.5-6.8 |
| Strong decay/waste/infestation, no bodily exposure | 2.5-3.5 | 4.0-5.2 |
| Mild or contained contamination | 3.5-4.5 | 3.4-4.4 |
| Strong attenuation (medical, specimen, fiction) | 3.8-5.0 | 3.2-4.2 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Decay**: Bread covered by green-black mold and moist discoloration in an open bag. ->
  spoiled food, widespread growth, ingestion relevance, no bodily exposure;
  activation_evidence []. **V 2.8, A 4.4**, strong.
- **Gore**: A close-up of a deep open wound with exposed tissue and fresh blood. -> severe
  bodily cue, high vividness and contact salience; activation_evidence ["fresh exposed
  tissue"]. **V 2.0, A 6.2**, strong.

## Output Contract

In the shared JSON separate cue type, extent/contact, realism, attenuation, and top-level
`activation_evidence` (empty list if none). Describe material, never label a person disgusting;
state identification uncertainty.
