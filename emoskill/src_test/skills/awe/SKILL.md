---
name: "awe"
description: "Analyzes awe-like VA elicited by visible physical vastness, extreme depth, vertical scale, or uncontrollable natural force. Use only when scale itself dominates; ordinary beauty or symbolic solemnity is insufficient."
---

# Awe
## Purpose
Infer awe from verifiable scale references, spatial overwhelm, and safety conditions. A need for cognitive accommodation cannot be proven from one image and may only be cautiously inferred when scale evidence is strong.
## Routing Card
USE WHEN:
- At least two independent scale cues are visible and the first response is immensity, depth, or uncontrollable force.
- The environment visibly dwarfs human references and promotes sustained viewing, admiration, or defensive withdrawal.
DO NOT USE WHEN:
- The scene is primarily calm, enterable, and low-demand rather than overwhelming.
- Solemnity comes from memorial, death, religion, or social meaning rather than physical scale.
VISUAL TRIGGERS:
- Tiny people or vehicles, extreme vertical drop, deep perspective, horizonless extension.
- Huge waves, storms, eruptions, waterfalls, or forces beyond individual control.
NEAR-MISS BOUNDARIES:
- Calm shorelines, forests, paths, or horizons -> `kaplan-art-restoration`.
- Human harm, disaster consequence, or concrete risk -> `cognitive-appraisal`.

## Core Constructs
- **Scale reference**: known-size objects such as people, vehicles, trees, windows, or doors compared with the dominant structure.
- **Spatial overwhelm**: depth, height, extension, or force exceeding ordinary human scale.
- **Self-diminishment**: the viewer or depicted person appears small, vulnerable, or low in control relative to the environment.
- **Safety–threat modulation**: safe viewing raises valence; exposure and approaching force raise arousal and lower valence.

## Use When
Use when scale relations and force remain the main affective explanation after removing color and generic beauty judgments.
## Do-Not-Use-When Rules
- Do not assign `strong` without a credible scale reference.
- Do not treat object quantity, broad themes, or wide-angle distortion as physical vastness.
- Do not claim that cognitive accommodation has been directly observed.

## Applicability
- **Strong**: at least two scale cues plus a credible reference, with scale clearly dominant.
- **Partial**: the scene is grand but references are limited, or restoration and beauty compete with scale.
- **Weak**: vastness is mostly implied by category, lens effect, or symbolism.
- **Not applicable**: no physical scale contrast or uncontrollable force; final VA equals Direct.

## Reasoning Steps
1. Identify known-size reference objects and report their position and image proportion.
2. Compare those references with mountains, architecture, sky, waterfalls, or natural force.
3. Check whether depth, vertical drop, extension, and field-of-view occupation converge.
4. Assess whether the viewing position is safe, protected, stable, and sufficiently distant.
5. Separate quiet immensity from approaching force, impact risk, or fall exposure.
6. Infer action tendency: sustained viewing and admiration versus retreat, defense, or escape.
7. Derive Valence from safety, light, and controllable distance; derive Arousal from scale contrast, exposure, and force imminence.
8. Test restoration and event appraisal as competing explanations before setting applicability and Direct weight.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Vast, safe, and visually harmonious | 7.5–9.6 | 5.7–8.0 |
| Vast and clearly overwhelming | 6.6–9.1 | 7.2–9.4 |
| Approaching force or fall exposure | 2.7–4.9 | 8.3–10.0 |
| Weak reference; merely spacious | 5.3–6.9 | 3.8–6.1 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- Awe is not synonymous with a beautiful landscape; visible scale relations are required.
- At low fit, do not force scores from the table; contract the result toward Direct VA.

## Worked Example
A tiny climber faces a huge waterfall: the human scale reference and vertical drop support self-diminishment, while a stable platform reduces direct threat. The skill candidate is positive and high-arousal; unclear human scale would reduce fit and pull the final result toward Direct.

## Output Format
Return fixed JSON with `direct_valence_score`, `direct_arousal_score`, `skill_candidate`, `applicability`, `blend_weight`, `observations`, `mechanism_chain`, `alternative_hypothesis`, final `valence_score`, `arousal_score`, and `confidence`.
