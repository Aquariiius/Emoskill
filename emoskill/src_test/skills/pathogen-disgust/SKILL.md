---
name: "pathogen-disgust"
description: "Analyzes how decay, contamination, bodily fluids, wounds, waste, spoiled organic matter, and infestation create rejection of contact, ingestion, or proximity through pathogen plausibility and transmission pathways."
---

# Pathogen Disgust
## Purpose
Infer possible pathogen or contamination risk from visible material state, then infer stopping ingestion, isolation, cleaning, and withdrawal. Do not make value judgments about people, illness, or disability.
## Routing Card
USE WHEN:
- Abnormal material state and an accessible transmission path are the most direct negative mechanism.
- The dominant tendency is do not touch, do not eat, isolate, or clean rather than evade an attack.
DO NOT USE WHEN:
- The main danger is animal attack, a human weapon, moral violation, or generic visual clutter.
- Food is fresh and appetitive, or a clinical or laboratory setting fully controls the material with no spill cue.
VISUAL TRIGGERS:
- Mold, rot, slime, pus, vomit, feces, open wounds, and corpse decomposition.
- Wetness, oozing, abnormal discoloration, tissue damage, dense infestation, and spreading boundaries.
NEAR-MISS BOUNDARIES:
- Attack morphology in snakes, spiders, or predators -> `evolved-fear-module`.
- Pain, responsibility, and helping relationships around an injured person -> `cognitive-appraisal`.

## Core Constructs
- **Contamination source**: food, tissue, bodily fluid, waste, corpse, standing water, or infestation.
- **Material abnormality and pathogen plausibility**: whether discoloration, mold, wetness, exudate, damage, and decay converge.
- **Transmission accessibility**: whether the source is exposed, touchable, ingestible, splashable, spreading, or near mouth and nose.
- **Control and avoidance**: whether sealing, protection, cleaning, and professional context block transmission and shape isolation or cleaning.

## Use When
Use only when the image supports where contamination is, how the material is abnormal, and how it might reach a body or food; missing two of these prevents Strong fit.
## Do-Not-Use-When Rules
- Do not describe a person, illness, or disability itself as disgusting.
- Do not identify red liquid as blood or a stain as infection without supporting cues.
- Fermentation, medical, scientific, and special-effects contexts require attenuation checks.

## Applicability
- **Strong**: a clear source, at least two material abnormalities, and an accessible transmission path.
- **Partial**: contamination is clear but localized, sealed, or professionally controlled.
- **Weak**: color, texture, or liquid identity is ambiguous and transmission is unclear.
- **Not applicable**: no pathogen or contamination mechanism; final VA equals Direct.

## Reasoning Steps
1. Locate the source and its relation to food, skin, mouth/nose, or living space.
2. Describe color, wetness, viscosity, boundary, exudate, damage, and spread.
3. Test whether multiple states jointly support decay, infection, or waste contamination rather than ordinary texture.
4. Specify transmission by touch, ingestion, splash, airborne spread, vector, or adjacent-surface contamination.
5. Assess distance, exposed area, contamination density, and uncontrolled spread.
6. Check sealing, cleaning, protection, medical, scientific, culinary, or fictional attenuation.
7. Compare contamination avoidance with attack fear and empathic sadness to identify the dominant action tendency.
8. Lower Valence from pathogen plausibility and severity; raise Arousal from proximity and uncontrolled spread, then blend with Direct.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Severe decay or fluid spill with direct contact | 1.6–3.0 | 6.4–8.9 |
| Clear but localized contamination | 2.7–4.2 | 4.9–7.2 |
| Mild suspicious discoloration; weak transmission | 4.2–5.3 | 3.5–5.5 |
| Well sealed or professionally controlled | 4.2–6.1 | 3.3–6.1 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- Disgust mainly motivates contact rejection and contamination management; attack avoidance belongs to the fear module.
- Ambiguous or controlled contamination requires a lower weight so the skill does not over-pull Direct toward negativity.

## Worked Example
Green fuzzy patches spread across a bread surface: material state supports mold and ingestion risk, producing disposal and avoidance. If the sample is sealed in a laboratory dish, fit becomes Partial and the final VA moves toward Direct.

## Output Format
Return fixed JSON with source, material state, pathogen inference, transmission path, control factors, avoidance tendency, Direct inputs, candidate VA, and final blended VA.
