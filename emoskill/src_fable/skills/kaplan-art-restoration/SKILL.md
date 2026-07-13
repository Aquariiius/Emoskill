---
name: "kaplan-art-restoration"
description: "Analyze restorative affect in enterable, low-demand environments using Kaplan's Attention Restoration Theory. Infer being-away, soft fascination, extent, compatibility, and demand from visible openness, depth, coherence, affordance, refuge, clutter, and threat. Do not use for isolated objects, overwhelming scale, hard stimulation, or person-centered events."
---

# Kaplan Attention Restoration Theory

## Applicability Gate

REQUIRED:
- An enterable or inhabitable environment is the dominant affective source.
- Visible spatial organization supports low-demand viewing, gentle exploration, rest, or recovery.
- At least three restorative variables are observable, including one spatial variable.

REJECT:
- Isolated object, product, texture, tabletop arrangement, or decorative still life.
- Overwhelming scale, violent force, dense novelty, threat, or person-centered action dominates.
- Calmness comes mainly from blankness or lack of content rather than environmental structure.

NEAR MISS:
- Immense scale and self-diminishment -> awe.
- Novelty, ambiguity, dense pattern, or hard fascination -> berlyne-arousal-pleasure.
- Human stakes or visible danger -> cognitive-appraisal.

## Visual Variables

- **Apparent openness/depth**: sky, horizon, layered distance, paths, perspective; never claim physical meters.
- **Enterability/affordance**: paths, seating, shelter, walkable surfaces, usable interiors.
- **Coherence/extent**: connected legible layout with enough visual world to explore mentally.
- **Soft fascination**: water, foliage, clouds, gentle light, repeating natural detail that holds attention without search.
- **Compatibility/refuge**: fit with resting, strolling, observing; prospect-refuge balance.
- **Attentional demand**: clutter, abrupt contrast, crowding, warning cues, threat.

## Inference Procedure

1. Confirm an environment, not an object or person, carries the affect; assess enterability.
2. Estimate openness, depth, coherence, and affordances from named monocular cues.
3. Separate soft fascination from Berlyne-style hard fascination; record clutter or spectacle.
4. Integrate evidence into restorative potential; drama, exposure, or crowding weakens it.
5. Judge VA with the anchors below; restoration means LOW arousal, not mild excitement.

## Arousal Gate

Restorative scenes are low-activation by definition: start near 3 and stay in 2.5-4.0 unless a
concrete activation cue is visible (moving water force, crowds, storm light). Scenic beauty,
rich detail, or wide views are NOT activation cues. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| Strong restorative environment, safe and coherent | 6.8-7.6 | 2.5-3.8 |
| Mild restorative environment, ordinary calm place | 6.0-7.0 | 3.2-4.4 |
| Scenic but somewhat stimulating (partial fit) | 6.0-7.2 | 4.4-5.4 |
| Weak fit | 5.0-6.0 | 3.5-4.5 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Calm**: A lakeside path curves through trees toward open water and distant hills in soft
  daylight; no people or obstacles. -> depth, walkable path, prospect+refuge, low demand;
  activation_evidence []. **V 7.3, A 3.0**, strong.
- **Partial**: A bright coastal overlook with wind-blown waves and a busy footpath. -> open and
  attractive but wind, motion, and crowding add demand; activation_evidence ["moving waves",
  "crowded path"]. **V 6.6, A 4.8**, partial.

## Output Contract

In the shared JSON report spatial cues, ART constructs, restorative potential, competing
stimulation, and top-level `activation_evidence` (empty list if none). Do not claim measured
dimensions, safety, or actual recovery.
