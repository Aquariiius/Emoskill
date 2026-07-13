---
name: "evolved-fear-module"
description: "Uses Öhman and Mineka's evolved fear-module account to analyze defensive VA elicited by attack morphology, readiness, imminence, and safety attenuation in snakes, spiders, scorpions, and large predators."
---

# Evolved Fear Module
## Purpose
Infer vigilance, withdrawal, and escape from visible attack capability and contact probability without claiming the species is objectively dangerous.
## Routing Card
USE WHEN:
- A fear-relevant animal is affectively central and attack, venom, ambush, or predatory morphology is clear.
- Animal form explains the response better than story, contamination, pet interaction, or cuteness.
DO NOT USE WHEN:
- The main threat comes from human weapons, mechanical accidents, or environmental hazards.
- Decay, infestation contamination, neotenic cuteness, safe pet context, or toy status dominates.
VISUAL TRIGGERS:
- Coiling, open mouth, fangs, stinger, claws, predatory gaze, crouch, lunge, and concealment.
- Close distance, direct orientation, sudden exposure, limited escape space, or an unobstructed attack path.
NEAR-MISS BOUNDARIES:
- Pests co-occurring with filth, decay, or transmission risk -> `pathogen-disgust`.
- Young animals, pet caregiving, or human interaction -> `baby-schema` / `cognitive-appraisal`.

## Core Constructs
- **Attack capability**: teeth, claws, stingers, body size, and predatory apparatus.
- **Attack readiness**: coiling, crouching, open mouth, muscle tension, and target orientation.
- **Imminence**: image proportion, distance, direction, sudden concealment release, and escape space.
- **Safety attenuation**: glass, cage, leash, handler, distance, toy form, or cartoon rendering.

## Use When
Use when animal morphology and posture alone, after removing story context, still produce vigilance and defensive readiness.
## Do-Not-Use-When Rules
- Do not classify every insect, reptile, or wild animal as high threat.
- Do not claim the species is truly venomous, certain to attack, or objectively dangerous.
- Toys, decorations, and obvious cartoons cannot receive Strong fit.

## Applicability
- **Strong**: at least two of attack morphology, readiness, and close range are clear, with no safety barrier.
- **Partial**: threat morphology is clear but glass, leash, distance, or pet context attenuates it.
- **Weak**: only category membership is present, or the animal is symbolic, toy-like, or distant.
- **Not applicable**: no fear-relevant animal morphology; final VA equals Direct.

## Reasoning Steps
1. Identify visible animal contour, posture, and attack apparatus without guessing hidden anatomy.
2. Determine whether attack apparatus is exposed, retracted, or oriented toward a person or camera.
3. Estimate readiness from coiling, crouching, open mouth, body tension, and motion blur.
4. Estimate imminence from image proportion, orientation, distance, concealment, and available escape space.
5. Check glass, cages, leashes, handlers, cartoons, and toy cues for safety attenuation.
6. Compare attack-harm and contamination-transmission explanations and identify the more direct evidence.
7. Infer vigilance, stopping approach, retreat, or escape as defensive action tendencies.
8. Lower Valence from expected harm and raise Arousal from readiness and imminence, then blend with Direct according to fit.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Close, directly oriented, clear attack readiness | 1.9–3.3 | 8.3–10.0 |
| Clear attack morphology but limited distance or direction | 3.0–4.6 | 6.1–8.3 |
| Protected by glass, leash, or distance | 4.4–6.1 | 3.8–6.4 |
| Toy, cartoon, or decorative animal | 5.3–6.6 | 2.1–4.4 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- Fear intensity depends jointly on possible harm and contact imminence; category membership alone cannot justify extreme VA.
- Strong safety attenuation requires Partial or Weak fit and a final result closer to Direct.

## Worked Example
A coiled snake faces the camera inside a glass enclosure: coiling and orientation raise the threat candidate, but glass blocks contact. Applicability is Partial, so final VA remains much closer to Direct than an unobstructed attack scene.

## Output Format
Return fixed JSON with animal morphology, attack apparatus, readiness, imminence, safety attenuation, fear/disgust boundary, Direct inputs, and blended final VA.
