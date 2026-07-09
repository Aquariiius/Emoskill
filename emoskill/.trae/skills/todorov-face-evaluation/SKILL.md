---
name: "todorov-face-evaluation"
description: "Analyzes face-dominant images using Oosterhof & Todorov's social evaluation dimensions: perceived trustworthiness/valence and dominance. Use for neutral, resting, or mildly expressive faces where structural first impression is the affective source. Do not use for strong expressions, social interaction, body posture, or context-driven emotion."
---

# Todorov Face Evaluation

## Purpose

Estimate the automatic first impression a face may evoke from visible structure: warmth/threat, trustworthiness, dominance, authority, and approach-avoidance. This is a structural face-impression skill, not expression recognition or personality judgment.

## Routing Card

USE WHEN:
- A specific human face is the dominant subject.
- Expression is neutral, resting, or only mildly expressive.
- Affect comes from structural first impression rather than situation, action, or clear emotion.

DO NOT USE WHEN:
- Strong expression, smile, crying, anger, fear, intimacy, touch, conflict, or social event drives affect.
- Body posture or situational stakes are primary.
- Baby schema, contamination, animal threat, restoration, aesthetics, or vastness is stronger.

VISUAL TRIGGERS:
- Eye region, brow, mouth at rest, jawline, facial width, maturity cues, softness/hardness, pose.
- Portrait, headshot, face-centered image with low contextual action.
- Mild expression where structure still appears to drive impression.

NEAR-MISS BOUNDARIES:
- Face in social event, danger, intimacy, or clear context -> cognitive-appraisal.
- Full-body posture dominates -> emotional-body-language.
- Infantile/neotenic features dominate -> baby-schema.

## Core Constructs

- **Trustworthiness/valence**: perceived intention to help or harm, inferred from structural resemblance to warmth or threat.
- **Dominance**: perceived capacity, power, maturity, or intimidation.
- **Approach-avoidance**: likely viewer tendency from trust and dominance combination.
- **Ethical framing**: this is perceived first impression, not real character, morality, competence, or intent.

## Use-When Rules

Use this skill only when the face remains the affective source after removing surrounding context. The model is strongest for photographic, clearly visible, neutral-to-mild faces.

## Do-Not-Use-When Rules

- Do not use for strong emotional expressions; use direct VA or appraisal if context matters.
- Do not use for intimate, conflictual, caregiving, performance, or social scenes where interaction changes meaning.
- Do not use for face fragments too occluded or stylized to judge structure confidently.
- Do not make claims about the actual person.

## Applicability

Strong:
- Face is dominant, clear, neutral/mild, and low-context.

Partial:
- Mild expression or context is present but structural impression still matters.

Weak:
- Expression, interaction, or context dominates; keep VA conservative and state scope mismatch.

## Reasoning Steps

1. Confirm the image is face-dominant and low-context.
2. Check expression strength; defer or mark weak if expression/context dominates.
3. Identify visible structural cues only.
4. Estimate trustworthiness/valence and dominance.
5. Combine them into perceived social impression.
6. Map impression to VA with ethical caution.

## VA Mapping

| Face Impression | Valence | Arousal |
|---|---:|---:|
| Warm, trustworthy, low dominance | 6.5-8.5 | 3.5-5.5 |
| Trustworthy and dominant/authoritative | 6.0-8.0 | 5.0-6.8 |
| Low trust, high dominance/intimidating | 2.5-4.5 | 6.0-8.0 |
| Neutral/unclear structure | 4.8-6.0 | 4.5-5.8 |
| Weak Todorov fit | keep near direct VA | keep conservative |

## Boundary Notes

- Todorov is not emotion recognition.
- Strong smiles, crying, visible fear/anger, or social context should not be reduced to facial structure.
- Demographic and identity-linked cues can bias impressions; avoid essentializing.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report face dominance, expression/context check, structural cues, trust/dominance estimate, ethical note, and VA mapping.
