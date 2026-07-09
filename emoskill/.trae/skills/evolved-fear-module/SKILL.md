---
name: "evolved-fear-module"
description: "Analyzes automatic fear responses to evolutionarily fear-relevant animals using Öhman & Mineka's evolved fear module account. Use for snakes, spiders, scorpions, large predators, and threat-like animal morphology when predation, venom, ambush, or attack cues dominate. Do not use for human weapons, general danger, contamination/disgust, cute baby animals, pets, toys, or symbolic animal imagery when threat morphology is weak."
---

# Evolved Fear Module

## Purpose

Estimate fear-like affect from visually prepared animal threats: snakes, spiders, scorpions, large predators, and similar forms that can trigger rapid threat detection. This skill models perceived automatic fear, not objective danger or zoological accuracy.

## Routing Card

USE WHEN:
- Dominant affective content is a snake, spider, scorpion, large predator, or fear-relevant animal form.
- Fear comes from ancestral threat morphology: coils, legs, fangs, claws, venom, predatory crouch, ambush, strike-readiness.
- The animal's body form is the primary affective source.

DO NOT USE WHEN:
- Threat is human, mechanical, environmental, or situational without a fear-relevant animal.
- Rot, infestation, wounds, bodily waste, disease, or contamination is the main cue.
- Cute baby animal, pet, cartoon, toy, decorative motif, or safe-distance context dominates.

VISUAL TRIGGERS:
- Serpentine body, arachnid leg spread, scorpion tail, fangs, claws, predatory eyes, crouch, lunge, concealment.
- Close proximity, direct orientation, strike-ready posture, escape difficulty.
- Realistic animal rendering rather than symbolic pattern alone.

NEAR-MISS BOUNDARIES:
- Human weapon, accident, or interpersonal danger -> cognitive-appraisal.
- Disease-vector pests, decay, or infestation -> pathogen-disgust.
- Neotenic/cute animal morphology -> baby-schema.

## Core Constructs

- **Fear-relevant category**: snake, spider, scorpion, large predator, or morphologically similar threat.
- **Threat imminence**: proximity, orientation, posture, concealment, readiness to strike or attack.
- **Preparedness**: typical viewers may rapidly detect these forms as threat-relevant.
- **Context attenuation**: glass, leash, handler, pet context, cartoon, toy, distance, or documentary framing lowers response.
- **Fear vs. disgust**: predation/attack implies fear; contamination/disease implies pathogen disgust.

## Use When

Use this skill when the animal form itself explains affect better than narrative context. The model responds to perceived morphology, not exact species identity.

## Do-Not-Use-When Rules

- Do not use for generic danger without a threat animal.
- Do not use for insects or pests when contamination is the main reaction.
- Do not use for cute or cared-for animals when baby schema or social context dominates.
- Do not claim real-world danger; estimate perceptual fear only.

## Applicability

Strong:
- Fear-relevant animal is central, realistic, and threat morphology/imminence is clear.

Partial:
- Threat animal is visible but attenuated by safety context, distance, pet framing, or ambiguity.

Weak:
- Animal is symbolic, decorative, toy-like, cute, distant, or not fear-relevant.

## Reasoning Steps

1. Identify animal type and fear-relevant morphology.
2. Assess threat imminence from posture, proximity, orientation, and concealment.
3. Check context attenuation and safety cues.
4. Distinguish fear from disgust, baby schema, or appraisal.
5. Map stronger imminence to lower valence and higher arousal.
6. State uncertainty from individual phobia variation and species ambiguity.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| High imminence, no attenuation | 1.8-3.0 | 7.5-9.5 |
| Moderate threat | 2.8-4.0 | 5.5-7.5 |
| Low threat or strong safety attenuation | 4.2-5.5 | 3.5-5.8 |
| Toy/cartoon/decorative | 5.0-6.0 | 2.0-4.0 |
| Weak fear-module fit | keep near direct VA | keep conservative |

## Boundary Notes

- This skill is not for all fear, only fear-relevant animal morphology.
- Context can attenuate but may not fully erase automatic threat response.
- Phobia sensitivity varies widely; report typical-viewer estimates.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report animal identification, threat morphology, imminence, attenuation, fear/disgust boundary, and VA mapping.
