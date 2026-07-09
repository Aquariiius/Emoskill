---
name: "pathogen-disgust"
description: "Analyzes revulsion and avoidance from visible contamination, decay, bodily waste, wounds, spoiled organic matter, infestation, or disease cues using pathogen disgust and behavioral immune system concepts. Use when pathogen/contamination risk is the dominant affective mechanism. Do not use for predator fear, moral disgust without visible contamination, fresh appetitive food, face/body emotion, restoration, aesthetics, or general threat."
---

# Pathogen Disgust

## Purpose

Estimate disgust-like affect from visible cues of contamination, disease, decay, bodily fluids, wounds, infestation, or spoiled organic matter. This skill models pathogen-avoidance perception, not moral judgment or objective medical risk.

## Routing Card

USE WHEN:
- Dominant cues signal contamination, disease, decay, bodily waste, wounds, spoiled food, corpse decay, or infestation.
- Viewer response is revulsion, rejection, withdrawal, or avoidance rather than fear, sadness, or aesthetic interest.
- Visible pathogen risk is the main affective mechanism.

DO NOT USE WHEN:
- Predator or attack threat dominates.
- Moral/social violation appears without visible contamination or disease cues.
- Food is fresh/appetitive, or professional/clinical/fictional context strongly reframes the cue.

VISUAL TRIGGERS:
- Rot, mold, slime, pus, vomit, feces, blood pooling, open wounds, corpse decay.
- Spoiled food, diseased tissue, parasites, infestation, pests associated with filth.
- Wetness, oozing, discoloration, bodily fluids, decomposing organic matter.

NEAR-MISS BOUNDARIES:
- Snake, spider, predator, or attack threat -> evolved-fear-module.
- Weapon, accident, social violation, or human stakes -> cognitive-appraisal.
- Abstract ugly/chaotic visuals without contamination -> berlyne-arousal-pleasure or no_specialized_skill.

## Core Constructs

- **Pathogen disgust**: avoidance response to visible infection or contamination cues.
- **Behavioral immune system**: perceptual system biased toward avoiding possible disease sources.
- **Contamination intensity**: mild stain/discoloration to severe decay, fluids, exposed tissue, or dense infestation.
- **Context attenuation**: medical, culinary fermentation, scientific specimen, or fictional/horror contexts can reduce or reframe disgust.
- **Fear vs. disgust**: attack threat implies fear; contamination threat implies disgust.

## Use When

Use this skill when visible contamination cues explain affect better than story, danger, composition, or person-centered emotion.

## Do-Not-Use-When Rules

- Do not use for moral disgust unless visible pathogen cues are present.
- Do not use for predatory animals unless decay/contamination is dominant.
- Do not use for fresh, desirable food or clean clinical presentation without aversive contamination cues.
- Do not label people as disgusting; describe viewer perception of cues with ethical caution.

## Applicability

Strong:
- Contamination/decay cues are central, visible, and affectively dominant.

Partial:
- Contamination cues exist but context attenuates or another mechanism competes.

Weak:
- Cues are symbolic, mild, ambiguous, or better explained by another skill.

## Reasoning Steps

1. Identify visible contamination cue type: decay, fluid, wound, waste, infestation, disease, spoiled organic matter.
2. Estimate contamination intensity: mild, moderate, or severe.
3. Check context attenuation: medical, culinary, scientific, fictional, or cleaned/controlled setting.
4. Distinguish disgust from fear, appraisal, or aesthetic aversion.
5. Map intensity and attenuation to VA.
6. Note ethical sensitivity for illness, injury, disability, or human subjects.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| Severe contamination, no attenuation | 1.5-2.8 | 5.5-7.8 |
| Moderate contamination | 2.5-3.8 | 4.5-6.8 |
| Mild contamination | 3.5-4.8 | 3.5-5.2 |
| Strong context attenuation | shift valence +1 to +2 | keep or slightly reduce |
| Weak pathogen-disgust fit | keep near direct VA | keep conservative |

## Boundary Notes

- Disgust arousal is often lower than fear arousal at comparable severity.
- Medical or scientific framing can attenuate disgust but does not always erase visceral response.
- Moral or social disgust belongs to appraisal unless contamination is visible.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report contamination cues, intensity, context attenuation, fear/disgust boundary, ethical note if relevant, and VA mapping.
