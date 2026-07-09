---
name: "kaplan-art-restoration"
description: "Analyzes restorative potential in natural or spatial environments using Kaplan's Attention Restoration Theory: being-away, soft fascination, extent, and compatibility. Use for enterable, low-demand settings that invite calm attention recovery. Do not use for isolated objects, tabletop/product compositions, high-stimulation aesthetics, person-centered emotion, or overwhelming awe."
---

# Kaplan Attention Restoration Theory

## Purpose

Estimate how likely an image is to feel mentally restorative: a low-demand environment that lets directed attention recover through being-away, soft fascination, extent, and compatibility. This is an environment skill, not a generic calmness detector.

## Routing Card

USE WHEN:
- The image is dominated by an enterable or inhabitable environment.
- The affect is calm, peaceful, low-demand, and compatible with attention recovery.
- Visible cues support being-away, soft fascination, spatial coherence, and gentle exploration.

DO NOT USE WHEN:
- The image is an isolated object, texture, product shot, tabletop scene, or decorative still life.
- The scene is visually intense, novel, complex, chaotic, threatening, or overwhelming.
- A person, face, body posture, social event, contamination cue, baby schema, or threat animal is the affective focus.

VISUAL TRIGGERS:
- Forests, gardens, coastlines, water, sky, trails, quiet rooms, benches, paths, open space, coherent layout.
- Gentle light, low clutter, refuge, walkability, foreground/background depth.
- A calm invitation to rest, recover, or explore without effort.

NEAR-MISS BOUNDARIES:
- Huge scale or self-diminishment -> awe.
- Visual novelty, pattern, design, or hard fascination -> berlyne-arousal-pleasure.
- Ordinary calm object without an inhabitable setting -> no_specialized_skill or weak Berlyne.

## Core Constructs

- **Being-away**: visible escape from routine demands or mental load.
- **Soft fascination**: attention is held gently, without pressure or high stimulation.
- **Extent**: the setting feels coherent and spacious enough to enter mentally.
- **Compatibility**: the setting affords likely rest, strolling, looking, sitting, or gentle exploration.
- **Low demand**: low clutter, low threat, low ambiguity, and low sensory intensity.

## Use When

Use this skill when the environment itself is the affective source. The viewer should plausibly feel calmer, more restored, or gently absorbed because of the setting.

## Do-Not-Use-When Rules

- Do not use for isolated objects or material textures; natural material is not enough.
- Do not use for dramatic spectacle, danger, or overwhelming scale.
- Do not use when a person's emotion or action is central.
- Do not use when visual stimulation is active, puzzling, or design-driven.

## Applicability

Strong:
- Enterable environment plus clear low-demand restorative cues.

Partial:
- Environment is present, but visual drama, people, or aesthetic stimulation competes.

Weak:
- Calmness comes from object simplicity, blankness, or lack of content rather than environment restoration.

## Reasoning Steps

1. Confirm an enterable environment is the dominant affective source.
2. Identify being-away, soft fascination, extent, and compatibility cues.
3. Check whether hard fascination, awe, threat, or person-centered affect is stronger.
4. Estimate restorative potential from visible evidence only.
5. Map high restoration to positive valence and low-to-moderate arousal.
6. Mark applicability weak if the image is merely calm but not environmental.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| Strong restorative environment | 7.0-8.8 | 2.8-4.8 |
| Mild restorative environment | 6.0-7.2 | 3.5-5.5 |
| Beautiful but somewhat stimulating | 6.0-8.0 | 5.0-6.5 |
| Weak environment fit | keep near direct VA | keep conservative |

## Boundary Notes

- Kaplan is about restorative environments, not all low-arousal images.
- Soft fascination differs from Berlyne's hard fascination: the former rests attention; the latter stimulates it.
- A calm horizon can be Kaplan when it feels restful; it becomes Awe only when scale overwhelms.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report restorative cues, ART dimensions, boundary checks, and VA mapping.
