---
name: "berlyne-arousal-pleasure"
description: "Uses Berlyne's collative variables as a theoretical frame, but operationalizes them through visible novelty relations, element density, ambiguity, incongruity, organization, and search load; it does not use an abstract inverted-U shortcut."
---

# Berlyne Arousal-Aesthetic Pleasure
## Purpose
Explain how concrete visual organization produces easy reading, structured exploration, sustained search, or sensory conflict when no stronger social, event, or biological mechanism dominates.
## Routing Card
USE WHEN:
- Affect is mainly driven by composition, organization, visible novelty, ambiguity, or incongruity.
- Terms such as interesting or chaotic can be decomposed into figure-ground, density, grouping, competition, and search evidence.
DO NOT USE WHEN:
- Semantic events, contamination, animal threat, faces, bodies, restoration, or vastness provide a stronger mechanism.
- The image is merely an ordinary object, single color, or low-information background without clear collative variables.
VISUAL TRIGGERS:
- High element or edge density, repetition and grouping, competing high-contrast foci, occlusion, and ambiguous contours.
- Relations that violate an internal visual regularity, localized novelty, or layouts requiring repeated attention shifts.
NEAR-MISS BOUNDARIES:
- Enterable, low-demand environments -> `kaplan-art-restoration`.
- Goals, responsibility, or consequences must be inferred -> `cognitive-appraisal`.

## Core Constructs
- **Novelty and incongruity**: visible objects, proportions, or relations that violate regularities established within the scene.
- **Complexity and density**: number of independent elements, edges, textures, text regions, and occlusions per area.
- **Ambiguity and resolvability**: whether multiple interpretations exist and whether further viewing stabilizes figure-ground organization.
- **Organization and search load**: whether alignment, repetition, grouping, and hierarchy reduce attention shifts and focal competition.

## Use When
Use only when the main VA can be explained through visible structure without relying on vague words such as beautiful, artistic, or atmospheric.
## Do-Not-Use-When Rules
- Do not use an inverted-U as a single-image reasoning shortcut.
- Do not equate high saturation or many colors with high arousal.
- If fewer than two concrete collative variables can be reported, applicability cannot exceed Weak.

## Applicability
- **Strong**: at least three organization or collative variables are clear and semantic mechanisms are weak.
- **Partial**: visual structure is important, but content, environment, or scale competes.
- **Weak**: only one color, texture, unusual object, or subjective aesthetic judgment is available.
- **Not applicable**: no operational visual-stimulation mechanism; final VA equals Direct.

## Reasoning Steps
1. First rule out event, biological threat, contamination, restoration, and vastness mechanisms.
2. Locate primary visual units, candidate subjects, foreground-background structure, and boundary clarity.
3. Assess the density and spatial distribution of elements, edges, textures, text, and occlusion.
4. Check whether alignment, repetition, symmetry, grouping, and hierarchy create a stable reading path.
5. Identify novelty, incongruity, and whether multiple high-contrast regions compete for attention.
6. Decide whether ambiguity resolves with inspection or continues to disrupt figure-ground stability.
7. Infer the viewing state: easy reading, structured exploration, sustained search, or sensory overload.
8. Derive Valence from successful organization and resolvability; derive Arousal from search, competition, and conflict, then anchor low-fit results to Direct.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Clear subject, stable hierarchy, low competition | 6.4–8.3 | 2.7–4.9 |
| Many elements but clear grouping and path | 6.6–8.9 | 4.6–7.0 |
| Ambiguity that resolves with inspection | 5.5–7.5 | 5.3–7.5 |
| High density, unstable figure-ground, sustained competition | 3.0–5.3 | 6.6–9.4 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- The original Berlyne name is retained, but execution uses concrete visible variables rather than an abstract curve.
- This is not a miscellaneous fallback; insufficient evidence requires Weak or Not applicable and a result near Direct.

## Worked Example
A colorful poster contains dense text, but heading hierarchy, grid alignment, and reading order are clear: density is controlled by organization, producing structured exploration rather than chaos. A vague judgment that it 'looks designed' would only support Weak fit.

## Output Format
Return fixed JSON reporting figure-ground separation, density, organization, competition, ambiguity, search load, Direct inputs, candidate VA, applicability weight, and final VA.
