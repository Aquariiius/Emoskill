---
name: "awe"
description: "Analyzes visible awe-relevant scenes where physical vastness, grandeur, or uncontrollable scale is the dominant affective mechanism. It maps perceived vastness, self-diminishment, safety/threat, and beauty into valence-arousal. Use only when scale itself is psychologically central; do not use for calm restorative scenery, symbolic solemnity, ordinary landscapes, or aesthetic complexity without overwhelming scale."
---

# Awe

## Purpose

Model awe-like affect from visible physical vastness: scenes that make the viewer or depicted humans feel small before immense scale. This skill operationalizes the observable part of awe, mainly perceived vastness and probable self-diminishment. It cannot directly verify "need for accommodation"; treat that as an inferred consequence only when scale is clearly overwhelming.

## Routing Card

USE WHEN:
- The scene is dominated by physically overwhelming vastness, grandeur, or scale.
- At least two scale cues are visible: tiny human reference, unbounded extension, vertical immensity, extreme depth, or uncontrollable natural force.
- The affect comes from wonder, sublimity, overwhelm, or self-diminishment caused by scale itself.

DO NOT USE WHEN:
- The scene is calm, restorative, or spacious but not overwhelming.
- The solemnity comes from memorial, burial, death symbolism, repetition, or social meaning rather than physical vastness.
- A face, body, social event, contamination cue, baby schema, threat animal, or ordinary object is the affective focus.

VISUAL TRIGGERS:
- Vast canyons, star fields, enormous mountains, massive architecture, storm systems, volcanic plumes, huge waterfalls, deep cliffs.
- Tiny figures or recognizable scale references dwarfed by the environment.
- Vertigo, exposure, violent natural force, or horizonless extension.

NEAR-MISS BOUNDARIES:
- Calm shoreline, forest, sky, garden, or horizon -> kaplan-art-restoration.
- Striking composition, pattern, or visual novelty without overwhelming scale -> berlyne-arousal-pleasure.
- Symbolic mortality, memorial meaning, disaster consequence, or human stakes -> cognitive-appraisal.

## Core Constructs

- **Perceived vastness**: visible scale, depth, extension, verticality, or force beyond ordinary human scale.
- **Self-diminishment**: viewer or depicted humans feel small relative to the stimulus; stronger with tiny human references.
- **Safety vs. threat**: safe grandeur feels uplifting; dangerous or uncontrollable grandeur lowers valence and raises arousal.
- **Beauty enhancement**: light, harmony, and scenic beauty raise valence when threat is low.
- **Operational limit**: the model estimates probable awe from visual scale; it does not prove a viewer's cognitive accommodation.

## Use When

Invoke this skill when scale itself is the primary driver of affect. The image should make a typical viewer think "this is immense" before they think "this is peaceful", "this is pretty", "this is sad", or "this is visually interesting".

## Do-Not-Use-When Rules

- Do not use for ordinary beautiful nature that mainly feels restful; use Kaplan.
- Do not use for repeated symbols, monuments, or historical/moral meaning unless physical scale overwhelms the viewer.
- Do not use for visual complexity, surreal style, or dramatic color alone; use Berlyne.
- Do not use for concrete human danger, grief, responsibility, or social consequence; use Cognitive Appraisal.

## Applicability

Strong:
- Multiple physical scale cues are visible, and vastness clearly dominates affect.

Partial:
- The scene is large or grand, but calm/restorative or aesthetic qualities compete with scale.

Weak:
- "Vastness" is mainly symbolic, conceptual, repeated, or inferred from context rather than physically visible.

## Reasoning Steps

1. Check whether physical scale, not symbolism or beauty alone, is the main affective driver.
2. Identify scale cues: depth, vertical immensity, extension, tiny figures, force, or exposure.
3. Estimate self-diminishment strength from visible scale references.
4. Decide safe, threatening, or mixed awe from danger and control cues.
5. Map to VA using the ranges below; do not force high arousal for quiet awe.
6. State the operational limitation if accommodation is only inferred.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| Safe positive awe, serene scale | 7.0-8.5 | 5.8-7.2 |
| Safe positive awe, strongly overwhelming scale | 7.0-8.8 | 7.2-8.8 |
| Mixed awe, beautiful but unsettling | 5.0-6.5 | 6.5-8.5 |
| Threat-based awe, uncontrollable force or exposure | 2.5-4.5 | 8.0-10.0 |
| Weak scale cue | keep near direct VA | keep conservative |

## Boundary Notes

- Awe is not a synonym for "beautiful landscape".
- Awe is not a synonym for "solemn" or "large number of meaningful objects".
- Calm positive awe can be moderate arousal; reserve very high arousal for threat, vertigo, violent force, or unmistakable overwhelm.
- If no specialized cue strongly fits, route to `no_specialized_skill` rather than forcing Awe.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report visible scale cues, awe type, self-diminishment evidence, safety/threat assessment, and the VA mapping.
