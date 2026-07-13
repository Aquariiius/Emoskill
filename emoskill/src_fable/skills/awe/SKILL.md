---
name: "awe"
description: "Analyze awe-like affect when overwhelming vastness, verticality, depth, or uncontrollable force dominates. Infer vastness, self-diminishment, and safe versus threatening awe from multiple scale cues. Do not use for ordinary scenic beauty, restorative space, symbolic solemnity, or complexity without human-scale overwhelm."
---

# Awe

## Applicability Gate

REQUIRED:
- Physical vastness or force is the primary affective mechanism, not merely beauty or spaciousness.
- At least two independent scale cues are visible: tiny reference figures, extreme verticality, unbounded extension, deep atmospheric perspective, or massive uncontrollable force.
- The scene plausibly produces self-diminishment, wonder, or sublime threat because of scale.

REJECT:
- Calm shoreline, forest, garden, room, or horizon that is restorative but not overwhelming.
- Monument, memorial, or symbolism whose meaning rather than physical scale drives affect.
- Dramatic color, novelty, or wide-angle style without reliable scale references.

NEAR MISS:
- Low-demand enterable scenery -> kaplan-art-restoration.
- Perceptual novelty or complex composition -> berlyne-arousal-pleasure.
- Disaster consequences or human stakes -> cognitive-appraisal.

## Visual Variables

- **Scale references**: people, vehicles, trees, or buildings that establish relative size.
- **Vertical immensity / depth**: towering peaks, walls, cliffs, canyon depth, layered distance.
- **Force/uncontrollability**: storms, eruptions, avalanches, violent water.
- **Exposure/proximity**: cliff-edge viewpoint, engulfing scale, escape difficulty.
- **Safety/beauty**: stable viewpoint, harmonious light, shelter, absence of immediate danger.

## Inference Procedure

1. Verify physical scale, not symbolism or beauty, is the dominant mechanism.
2. List independent scale cues; reject lens drama without reference objects.
3. Estimate self-diminishment from the human-vs-environment disparity.
4. Classify safe awe, threat awe, or mixed from exposure, force, and shelter cues.
5. Judge VA with the anchors; quiet distant vastness is only moderately activating.

## Arousal Gate

Vastness alone is NOT an activation cue. Raise arousal above 5 only for visible force in
motion, engulfing proximity, exposure, or loss of control; a stable, distant, serene panorama
sits near 4.5-5.5. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| Safe awe, serene distant vastness | 6.8-7.8 | 4.4-5.6 |
| Safe awe, engulfing or dramatic scale | 6.6-7.6 | 5.6-6.6 |
| Threat awe: violent force, exposure, no control | 3.0-4.5 | 6.0-7.5 |
| Weak scale evidence | 5.0-6.0 | 4.0-5.0 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Safe**: Two tiny hikers on a stable overlook face an immense glacier valley in clear light.
  -> scale disparity, layered depth, no force or exposure; activation_evidence []. Serene safe
  awe. **V 7.4, A 5.0**, strong.
- **Threat**: A towering storm wall advances over a small coastal town, lightning visible. ->
  vertical mass, uncontrollable force in motion, engulfing proximity; activation_evidence
  ["advancing storm front", "lightning"]. **V 3.8, A 6.8**, strong.

## Output Contract

In the shared JSON report two scale cues, vastness/self-diminishment, awe branch,
safety/exposure modifiers, and top-level `activation_evidence` (empty list if none).
Accommodation is inferred, never observed.
