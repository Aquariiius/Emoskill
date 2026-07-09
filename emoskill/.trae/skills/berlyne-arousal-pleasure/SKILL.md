---
name: "berlyne-arousal-pleasure"
description: "Analyzes aesthetic stimulation with Berlyne's collative variables: novelty, complexity, ambiguity, incongruity, and surprise. Use when perceptual or compositional stimulation is the affective driver. Do not use for ordinary low-stimulation objects, restorative environments, narrative threat, face/body emotion, or specialized cues better handled by another skill."
---

# Berlyne Arousal-Aesthetic Pleasure

## Purpose

Estimate affect from visual stimulation itself: how novelty, complexity, ambiguity, incongruity, surprise, pattern, or design creates arousal potential and hedonic value. This skill is for perceptual/aesthetic mechanisms, not narrative emotion or generic object analysis.

## Routing Card

USE WHEN:
- Affect is driven by visible novelty, complexity, ambiguity, incongruity, surprise, pattern density, or design.
- The image invites active visual engagement or hard fascination.
- Object, artwork, architecture, design, abstract form, or arrangement is the affective focus.

DO NOT USE WHEN:
- The image is a mundane object or still life with no meaningful collative variable.
- The scene is a calm restorative environment.
- Affect is driven by situation, threat, face, body posture, contamination, baby schema, threat animal, or overwhelming scale.

VISUAL TRIGGERS:
- Unusual composition, abstract form, visual density, puzzling arrangement, high contrast, rich pattern, incongruity.
- Stylized artwork, striking design, surreal elements, perceptual ambiguity.
- Stimulation that can be pleasant, boring, or overwhelming depending on intensity.

NEAR-MISS BOUNDARIES:
- Low-demand natural/spatial environment -> kaplan-art-restoration.
- Human stakes, danger, social meaning, or narrative ambiguity -> cognitive-appraisal.
- Plain low-stimulation object -> no_specialized_skill or weak Berlyne.

## Core Constructs

- **Collative variables**: novelty, complexity, ambiguity, incongruity, and surprise.
- **Arousal potential**: how much active perceptual processing the image demands.
- **Hedonic value**: pleasure follows a rough inverted-U; too little is flat, moderate is engaging, excessive can be aversive.
- **Psychophysical intensity**: contrast, saturation, density, and scale can raise arousal but do not define the skill alone.

## Use When

Use this skill when perceptual stimulation explains affect better than what the image depicts narratively. A static object can qualify only if its arrangement, style, ambiguity, or design is genuinely salient.

## Do-Not-Use-When Rules

- Do not use for ordinary object shots just because they are composed.
- Do not use for threat scenes where arousal comes from danger.
- Do not use for calm nature/spaces where attention is restored rather than stimulated.
- Do not use when a specialized biological or social mechanism is clearer.

## Applicability

Strong:
- One or more collative variables clearly dominate affect.

Partial:
- Aesthetic stimulation is present but competes with narrative, environment, or scale.

Weak:
- The image is visually simple, familiar, and low in novelty/complexity; keep VA close to direct baseline.

## Reasoning Steps

1. Confirm that affect is perceptual/compositional rather than narrative or restorative.
2. Identify salient collative variables and sensory intensity.
3. Estimate arousal potential: low, moderate, or excessive.
4. Place the image on the inverted-U.
5. Infer hedonic value from arousal potential and visible tone.
6. Mark weak applicability when collative variables are trivial.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| Low stimulation, familiar/simple | 4.8-5.8 | 2.5-5.0 |
| Moderate stimulation, engaging | 6.0-8.0 | 5.0-7.0 |
| Excessive stimulation, chaotic/aversive | 2.5-5.0 | 7.0-9.0 |
| Somber aesthetic stimulation | 3.0-5.5 | 5.0-7.5 |
| Weak Berlyne fit | keep near direct VA | keep conservative |

## Boundary Notes

- Berlyne is not a fallback for every object image.
- "Interesting composition" must be visibly supported by non-trivial collative variables.
- Repetition counts only when it creates real perceptual engagement, not merely order.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report collative variables, arousal potential, inverted-U position, boundary checks, and VA mapping.
