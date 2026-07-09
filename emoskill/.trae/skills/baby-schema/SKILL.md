---
name: "baby-schema"
description: "Analyzes cuteness and caregiving affect from infantile morphology using Lorenz's baby schema / Kindchenschema: large head, high forehead, large low-set eyes, round face, chubby cheeks, small nose/mouth, short limbs, and soft proportions. Use when neotenic form is the dominant affective mechanism. Do not use when danger, distress, uncanny qualities, adult face structure, body emotion, or situation meaning dominates."
---

# Baby Schema / Kindchenschema

## Purpose

Estimate affect from visible infantile or neotenic morphology. Baby schema features tend to elicit cuteness, tenderness, approach, and caregiving motivation. This skill applies to human infants, baby animals, and deliberately neotenic designed characters or products when form, not story, drives affect.

## Routing Card

USE WHEN:
- The dominant subject is a human infant, baby animal, or deliberately neotenic character/object.
- Affect is cuteness, tenderness, protectiveness, warmth, or caregiving motivation.
- Infantile morphology is more important than surrounding situation or expression.

DO NOT USE WHEN:
- The subject is an adult neutral/mild face; use todorov-face-evaluation.
- The infantile subject is visibly in danger, distress, pain, illness, or exploitation; use cognitive-appraisal.
- The affect comes from uncanny wrongness, body posture, contamination, predatory threat, or aesthetic style rather than baby schema.

VISUAL TRIGGERS:
- Large head-to-body ratio, high forehead, round face, large low-set eyes.
- Chubby cheeks, small nose/mouth, short limbs, rounded body, soft plush-like proportions.
- Infant, cub, puppy/kitten-like morphology, kawaii/chibi/neotenic design.

NEAR-MISS BOUNDARIES:
- Adult baby-faced portrait -> todorov-face-evaluation unless infantile design is explicit.
- Cute subject in danger or distress -> cognitive-appraisal.
- Cute animal with predator/threat morphology dominant -> evolved-fear-module.

## Core Constructs

- **Baby schema load**: number and strength of infantile features.
- **Cuteness perception**: likely viewer response of "cute", "adorable", or tender.
- **Caregiving motivation**: approach, protect, nurture, hold, or help.
- **Context safety**: cute response is strongest when the subject appears safe and benign.
- **Uncanny or distress override**: eerie, injured, exploited, or endangered subjects can flip valence.

## Use When

Use this skill when morphology is the affective source. The key question is whether visible proportions, not narrative context, create a caregiving/cuteness response.

## Do-Not-Use-When Rules

- Do not use for adult face evaluation except weak/partial neoteny notes.
- Do not rate vulnerable subjects as "cute" when danger, suffering, or exploitation dominates.
- Do not use for animal threat, contamination, or posture-driven emotion.
- Do not infer real health, development, personality, or worth from appearance.

## Applicability

Strong:
- Multiple baby schema features are clear and the context is safe/benign.

Partial:
- Some neotenic cues are present, but age/species/design or context weakens the effect.

Weak:
- Cuteness is culturally learned, stylistic, or secondary to another affective mechanism.

## Reasoning Steps

1. Identify subject type: infant, baby animal, neotenic design, or weak adult neoteny.
2. List visible baby schema features and estimate load.
3. Check safety, distress, danger, exploitation, or uncanny override.
4. Estimate likely cuteness/caregiving response.
5. Map safe baby schema to positive valence and low-to-moderate arousal.
6. Mark partial/weak when morphology is not the main affective driver.

## VA Mapping

| Case | Valence | Arousal |
|---|---:|---:|
| High baby schema, safe/benign | 8.0-9.2 | 3.5-5.8 |
| Moderate baby schema, safe/benign | 7.0-8.2 | 3.0-5.0 |
| Mild/partial baby schema | 6.0-7.2 | 3.0-5.0 |
| Extreme cuteness / cute aggression | 8.5-9.5 | 5.0-6.8 |
| Distress, danger, or uncanny override | 2.0-5.0 | 4.5-7.5 |
| Weak baby-schema fit | keep near direct VA | keep conservative |

## Boundary Notes

- Baby schema is about morphology, not simply young age or positive content.
- Safety strongly conditions the cuteness response.
- Designed characters can qualify if neotenic proportions are visible.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report subject type, baby schema features, load, context override check, caregiving/cuteness response, and VA mapping.
