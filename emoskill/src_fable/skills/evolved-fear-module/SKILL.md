---
name: "evolved-fear-module"
description: "Analyze prepared fear responses to realistic fear-relevant animals when threat morphology and imminence drive affect. Infer realism, proximity, orientation, attack readiness, concealment, and safety attenuation before VA. Do not use for generic danger, contamination-dominant pests, cute animals, pets, toys, or symbolic imagery without credible threat."
---

# Evolved Fear Module

## Applicability Gate

REQUIRED:
- A snake, spider, scorpion, large predator, or closely related threat morphology is visually central.
- The animal form itself, not story or contamination, plausibly drives rapid threat perception.
- At least one imminence cue beyond category membership is visible.

REJECT:
- Human, mechanical, environmental, or social danger without a fear-relevant animal.
- Infestation, decay, or bodily contamination dominates the response.
- Toy, cartoon, decoration, distant documentary subject, cared-for pet, or neotenic animal.

NEAR MISS:
- Pest associated with filth or disease -> pathogen-disgust.
- Young/cute animal morphology -> baby-schema.
- Human handling, accident, or conflict determines affect -> cognitive-appraisal.

## Visual Variables

- **Threat morphology**: coils, leg spread, fangs, claws, predatory crouch, strike posture.
- **Realism**: photographic/biological form versus illustration, toy, costume, or pattern.
- **Proximity/orientation**: frame occupancy, facing the viewer, raised head, lunge, stalking.
- **Concealment/surprise**: camouflage, ambush position, sudden foreground emergence.
- **Escape/control**: barriers, glass, leash, handler, distance, or apparent entrapment.

## Inference Procedure

1. Qualify the animal and its visible threat morphology; no objective-danger claims.
2. Estimate realism; symbolic or toy-like forms sharply reduce applicability.
3. Estimate imminence from proximity, orientation, posture, concealment, escape cues.
4. Check attenuation (enclosure, distance, handler) and competing mechanisms.
5. Judge VA with the anchors. Category alone NEVER produces high threat scores.

## Arousal Gate

Fear arousal requires visible imminence: strike posture, close proximity, direct orientation,
or blocked escape. A fear-relevant animal that is merely present, resting, distant, or behind a
barrier is NOT an activation cue by itself. No imminence cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| High imminence: close, oriented, strike-ready, no barrier | 3.0-4.0 | 6.0-7.5 |
| Visible threat animal, calm posture, moderate distance | 4.0-5.0 | 4.5-5.5 |
| Strong attenuation: enclosure, leash, far distance | 4.5-5.5 | 3.5-4.5 |
| Toy, cartoon, decorative, weak fit | 5.0-6.0 | 3.0-4.0 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral. Most viewers rate even real snakes/spiders nearer 4 than 2 in
valence; reserve V < 3 for converging imminence.

## Worked Examples

- **Imminent**: A rattlesnake fills the frame, coiled, head raised toward the camera, rattle
  lifted. -> realistic morphology, close, oriented, strike-ready; activation_evidence ["strike
  posture", "close proximity", "facing viewer"]. **V 3.4, A 6.8**, strong.
- **Attenuated**: A realistic snake rests coiled behind terrarium glass at moderate distance,
  mouth closed. -> category present, no strike, barrier visible; activation_evidence [].
  **V 4.7, A 4.3**, partial.

## Output Contract

In the shared JSON separate category, realism, imminence, attenuation, and barriers, plus
top-level `activation_evidence` (empty list if none). Never infer venom, intent, or attack
probability.
