---
name: "kaplan-art-restoration"
description: "Analyzes images with Kaplan's Attention Restoration Theory (being-away, soft fascination, extent, compatibility) and maps restorative potential into valence-arousal. Use for natural or spatial environments where the affect is calm, restful, coherent, and low-demand — scenes that hold attention effortlessly (soft fascination) rather than stimulate it. Do NOT use for scenes that are visually novel, complex, chaotic, or intensely stimulating (hard fascination / high arousal potential) — use Berlyne instead. Do NOT use when a person's situational emotion, not the environment, is the point of the image — use Cognitive Appraisal or PANAS. Do NOT use for face-centered structural impressions (Todorov)."
---

# Kaplan Attention Restoration Theory

## Purpose

Use this skill when an image's affect is best explained by its restorative potential — its capacity to give a viewer a mental break from effortful, directed attention. Kaplan's theory distinguishes **soft fascination** (gentle, low-effort stimuli like flowing water, drifting clouds, rustling leaves, which hold attention without draining it and leave room for reflection) from **hard fascination** (highly stimulating, attention-demanding content like sports, spectacle, or dramatic complexity, which fully captures attention and affords little reflective capacity). ART's restorative effect depends specifically on soft fascination — this skill is about that calm, low-arousal register, not stimulation in general.

## Core Constructs

- **Being-away** — psychological or physical distance from routine demands and everyday concerns; a sense of escape.
- **Fascination (soft)** — attention held effortlessly and pleasantly, without cognitive strain, leaving room for reflection (as opposed to hard fascination, which is stimulating and demands engagement).
- **Extent** — sufficient scope and coherence that the environment feels like "another world," inviting exploration rather than fragments.
- **Compatibility** — a good fit between what the setting affords and what a viewer would want to do there.

## Use When

Invoke this skill when:

- The image is dominated by a natural or spatial environment (landscape, garden, water, sky, forest, coastline, restorative interior) rather than a person's expressed emotion.
- The plausible affect is calm, restful, peaceful, or quietly absorbing — consistent with soft fascination — rather than exciting, dramatic, or visually overwhelming.
- The scene reads as coherent and spacious enough to feel immersive (extent), and inviting rather than jarring (compatibility).
- The task concerns restoration, mental recovery, calmness, or environmental preference specifically.

## Do-Not-Use-When Rules

Do not use this skill when:

- The scene is novel, visually complex, ambiguous, chaotic, or intensely stimulating — high collative arousal potential rather than soft, restful fascination → defer to **Berlyne**.
- A person's expressed or situational emotion is the actual focus of the image, with the environment merely as backdrop → defer to **PANAS** (if legible from expression) or **Cognitive Appraisal** (if situational inference is needed).
- A face is the dominant subject → defer to **Todorov**.
- The setting is demanding, cluttered, urban-frantic, or otherwise effortful to take in — this is the opposite of what ART predicts as restorative.

## Routing / Self-Check

Before proceeding:

1. **Is the environment (not a person) the dominant affective content?** If a person's expression/situation is the real subject, defer to PANAS/Appraisal/Todorov as appropriate.
2. **Does the scene read as calm and effortlessly engaging (soft fascination), or as novel/complex/stimulating (hard fascination)?** If the latter, defer to Berlyne — this is the key discriminator between the two environment-focused skills.
3. If the scene is environment-dominant and plausibly restful/coherent, proceed.

State which check applied in the output.

## Reasoning Steps

1. **Self-check routing** — confirm this is genuinely a restorative-environment case, not a stimulation-driven or person-focused one; if not, name the better-fitting skill.
2. Describe the environment and its visible affordances (openness, greenery, water, light, spatial coherence, presence/absence of people).
3. Estimate being-away, soft fascination, extent, and compatibility from visible evidence, noting which are strongly vs. weakly supported.
4. Explain whether the scene likely supports restoration of directed attention or instead demands effortful engagement (a sign it may actually belong to Berlyne).
5. Infer the likely affective consequence for a viewer (calm, refreshed, at ease) versus alternatives.
6. Convert the restorative judgment into final VA, favoring low-to-moderate arousal and positive valence when ART's conditions are well met.

## Output Format

```
ROUTING CHECK: [why this is a restorative-environment case, not stimulation-driven or person-focused]
VISIBLE RESTORATIVE CUES: [environment description: greenery, water, light, openness, coherence, incidental people if any]
ART DIMENSIONS: [being-away / soft fascination / extent / compatibility, each with supporting evidence]
FASCINATION TYPE CHECK: [soft (restful) vs. hard (stimulating) — explicit judgment, since this is the Berlyne boundary]
RESTORATIVE POTENTIAL: [likely affective consequence for a viewer]
FINAL VALENCE: [value + justification]
FINAL AROUSAL: [value + justification, typically low-to-moderate for restorative scenes]
UNCERTAINTY NOTES: [ambiguity, mixed cues, incidental people, image quality]
```

## Uncertainty and Ethical Constraints

Restorative potential is a *likely perceptual effect on a typical viewer*, not a guaranteed or universal response — individual preferences, cultural background, and personal associations with a setting vary (compatibility is inherently person-relative). Avoid absolute claims like "this scene is restorative"; prefer "this scene is likely to be experienced as restorative by many viewers, because...". If people are present, do not speculate about their specific emotions or personalities — treat them as incidental to the environment unless the task specifically shifts focus to them (in which case, defer per the routing rules).

## Examples That Should Trigger

- A quiet forest trail with dappled light and no clutter.
- A wide, calm lake at dawn with mist and still water.
- A minimalist garden courtyard with a bench and greenery.

## Examples That Should NOT Trigger

- A dense, chaotic urban street market bursting with color and movement → Berlyne (hard fascination/high collative arousal).
- A dramatic thunderstorm over a churning ocean → Berlyne (high arousal potential, not restful).
- A hiker who looks visibly distressed on an otherwise calm trail → Cognitive Appraisal/PANAS (person's emotion is the point).
- A close-up neutral portrait with a blurred natural background → Todorov (face is dominant).

## Ambiguous Cases

- **Beautiful but dramatic landscape (e.g., dramatic canyon, crashing waterfall):** if the scene is visually striking/novel/complex enough that it demands attention rather than resting it, lean Berlyne; if it reads as expansive but calm and coherent, lean Kaplan. State which fascination type dominates and note the alternative reading.
- **Landscape with incidental people:** if people are small/background, proceed with Kaplan, noting their presence briefly; if their activity or expression becomes the focal point, defer to PANAS/Appraisal.
- **Restorative interior with aesthetic flourishes:** if the calming, low-effort quality dominates, use Kaplan; if the aesthetic composition itself is the striking element, consider whether Berlyne is a better fit and note the ambiguity.
