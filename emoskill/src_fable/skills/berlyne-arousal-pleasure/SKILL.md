---
name: "berlyne-arousal-pleasure"
description: "Analyze perceptual affect using Berlyne's collative variables: complexity, novelty, ambiguity, incongruity, order, and processing fluency. Progress from visible composition to arousal potential and hedonic judgment. Do not route ordinary objects, narrative emotion, restorative space, vastness, or biological cues merely because an image is artistic or detailed."
---

# Berlyne Arousal-Pleasure

## Applicability Gate

REQUIRED:
- Perceptual or compositional stimulation, not depicted story or object category, is the primary mechanism.
- At least two collative variables have visible support, or one is exceptionally dominant.
- The image demands active visual organization, comparison, or resolution.

REJECT:
- Ordinary product, object, still life, or familiar scene with trivial organization.
- Arousal is better explained by danger, body action, contamination, infantile morphology, or social stakes.
- Calm enterable space or overwhelming scale better fits Kaplan or Awe.

NEAR MISS:
- Low-demand coherent environment -> kaplan-art-restoration.
- Vastness and self-diminishment -> awe.
- Narrative ambiguity about actors and consequences -> cognitive-appraisal; perceptual ambiguity stays here.

## Visual Variables

- **Element density / feature variety**: distinct forms, boundaries, colors, orientations, textures, judged ordinally.
- **Order/regularity**: symmetry, repetition, alignment, hierarchy, rhythm, grouping.
- **Perceptual ambiguity / incongruity**: multiple figure-ground readings, incompatible forms, violated expectation.
- **Sensory intensity**: contrast, saturation, sharp transitions, crowding.
- **Processing fluency**: whether structure resolves into groups versus unresolved overload.

## Inference Procedure

1. Confirm affect comes from visual organization; exclude narrative, restorative, scale, biological mechanisms.
2. Describe density, variety, order, ambiguity, incongruity, intensity with visible anchors.
3. Integrate into arousal potential; detail alone is insufficient.
4. Estimate fluency from hierarchy and resolvability; engaging complexity versus chaotic overload.
5. Judge VA with the anchors. Viewing art is a CALM activity by default.

## Arousal Gate

Looking at a static composition rarely activates the body: most artwork and design sits at
3.5-5.0 arousal. Complexity, detail, saturation, and interestingness are NOT activation cues.
Raise arousal above 5.5 only for genuinely unresolvable overload or aggressive sensory assault
(strobing contrast, crowding that resists grouping). No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| Fluent, engaging stimulation (resolvable complexity) | 5.5-6.6 | 4.0-5.2 |
| Striking incongruity/surprise, still processable | 5.5-6.5 | 5.0-5.8 |
| Chaotic or aversive overload, low fluency | 3.5-4.5 | 5.4-6.4 |
| Low stimulation, simple or familiar | 4.5-5.5 | 2.8-4.0 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Engaging**: An abstract poster with many irregular high-contrast shapes organized by
  repeated alignments and a clear hierarchy. -> high variety, moderate density, fluent grouping;
  activation_evidence []. **V 6.2, A 4.6**, strong.
- **Overload**: A collage packed edge-to-edge with clashing colors and no discernible grouping
  or focus. -> extreme density, no fluency, aversive crowding; activation_evidence
  ["unresolvable visual crowding"]. **V 4.0, A 5.8**, strong.

## Output Contract

In the shared JSON separate observable composition, arousal potential, processing fluency,
competing mechanisms, and top-level `activation_evidence` (empty list if none). Never invoke
the inverted-U before documenting stimulation and fluency.
