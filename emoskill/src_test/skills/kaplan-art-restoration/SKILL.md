---
name: "kaplan-art-restoration"
description: "Uses Kaplan's Attention Restoration Theory to analyze how being-away, soft fascination, extent, compatibility, and low cognitive demand in enterable environments produce restorative VA."
---

# Kaplan Attention Restoration Theory
## Purpose
Determine whether an environment supports low-effort attention, gentle exploration, and temporary relief from task demands. Nature, green color, or quietness alone does not prove restoration.
## Routing Card
USE WHEN:
- An enterable or mentally enterable environment is the primary affective source.
- The scene offers soft fascination, coherent space, and safe opportunities to rest, stroll, or look around.
DO NOT USE WHEN:
- An isolated object, human event, direct danger, overwhelming scale, or dense visual conflict dominates.
- Calmness comes only from blankness, low saturation, or lack of content rather than environmental support.
VISUAL TRIGGERS:
- Continuous paths, water, canopy, open views, benches, clear foreground-middle-background depth, and low crowding.
- Gentle light, low search demand, places to sit, and spaces without urgent vigilance.
NEAR-MISS BOUNDARIES:
- Human references are strongly dwarfed by the environment -> `awe`.
- Organization, density, and visual competition dominate -> `berlyne-arousal-pleasure`.

## Core Constructs
- **Being-away**: visible removal from work, traffic, crowding, and task cues.
- **Soft fascination**: water, leaves, clouds, or light gently hold attention without sustained search.
- **Extent**: coherent depth and spatial continuation that can be mentally entered and explored.
- **Compatibility and low demand**: support for sitting, walking, viewing, or gentle exploration with clear routes and safety.

## Use When
Use when the image can answer, with concrete spatial evidence, whether a person could safely remain or explore slowly without sustained vigilance or problem solving.
## Do-Not-Use-When Rules
- Blue, green, natural categories, or spaciousness alone cannot support Strong restoration.
- Cliff exposure, storms, crowding, interrupted paths, and unclear exits reduce restoration.
- Non-enterable textures, product shots, and tabletop still life are not restorative environments.

## Applicability
- **Strong**: at least three of enterability, soft fascination, extent, and compatible activity are clear.
- **Partial**: restorative cues exist but people, drama, crowding, or scale competes.
- **Weak**: only color, a nature category, or generic calmness is visible.
- **Not applicable**: no environment that supports staying or movement; final VA equals Direct.

## Reasoning Steps
1. Determine whether the viewer can imagine entering the scene rather than viewing a flat texture or distant object.
2. Describe foreground-middle-background structure, paths, occlusion, views, seating, and movement possibilities.
3. Identify soft-fascination sources and check whether they demand active search or sustained vigilance.
4. Check whether work cues, traffic, crowding, noise implications, or task objects undermine being-away.
5. Identify supported low-demand activities and whether their routes are safe and continuous.
6. Test overwhelming scale, self-diminishment, and visual processing load as alternatives.
7. Derive Valence from safety, compatibility, and environmental affinity; derive lower Arousal from low vigilance and low search demand.
8. Set applicability from ART evidence coverage and pull category-based 'nature equals restoration' judgments toward Direct.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Enterable, coherent, safe, and low-demand | 7.8–9.8 | 2.4–4.6 |
| Restorative cues with mild crowding or drama | 6.6–8.7 | 4.2–6.1 |
| Nature category but unclear path, staying, or safety | 5.5–7.2 | 3.8–5.7 |
| Sustained vigilance or visible environmental danger | 3.3–5.5 | 6.1–8.9 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- Restoration depends on staying, exploring, and low task demand; it is not a label for every low-arousal image.
- With only one or two weak environmental cues, use Weak weight so the final result remains mainly Direct.

## Worked Example
A forest path follows a calm stream with a bench in the foreground: path continuity, soft water motion, spatial extent, and rest affordance jointly support Strong restoration. A featureless green field without entry cues would only support Weak fit.

## Output Format
Return fixed JSON with enterability, the four ART constructs, disruptive factors, afforded activity, Direct inputs, candidate VA, applicability weight, and final VA.
