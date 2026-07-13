---
name: "todorov-face-evaluation"
description: "Analyzes perceived trustworthiness/social valence and dominance in face-dominant images using Oosterhof and Todorov's social-evaluation dimensions, with expression, pose, and context gates that prevent appearance-based impressions from being treated as real personality."
---

# Todorov Face Evaluation

## Purpose

Estimate the structural first impression elicited by a neutral, resting, or mildly expressive face. This skill describes a viewer's possible social perception only; it does not judge the person's actual trustworthiness, ability, morality, or intent.

## Routing Card

USE WHEN:
- One clear human face dominates the image, while surrounding action and social context are weak.
- The expression is neutral, resting, or mild, and structural appearance can still independently influence VA.

DO NOT USE WHEN:
- Strong smiling, crying, anger, fear, pain, or social interaction dominates.
- Body posture, weapons, intimacy, conflict, injury, or event consequences determine the primary meaning.

VISUAL TRIGGERS:
- Resting configuration of the eye-brow and mouth regions, facial maturity, jaw shape, facial width, and head pose.
- Direct or averted gaze, low-context portraits, and facial movements of limited intensity.

NEAR-MISS BOUNDARIES:
- Expression or event meaning requires interpretation of goals and consequences -> `cognitive-appraisal`.
- Bodily expression remains complete after the face is occluded -> `emotional-body-language`.

## Core Constructs

- **Expression gate**: separate dynamic expressive actions from relatively stable facial structure before evaluating social impressions.
- **Perceived trustworthiness/social valence**: the warmth-to-threat direction conveyed in a first impression, not the person's real character.
- **Perceived dominance**: apparent maturity, strength, authority, or intimidation, not actual ability.
- **Approach-avoidance integration**: how perceived trustworthiness and dominance jointly influence social approach or vigilance.

## Use When

After removing the background, the face remains the affective center, and relatively stable structural social impressions still make a visible contribution after explicit expressive actions are considered separately.

## Do-Not-Use-When Rules

- When a strong expression is present, applicability must not exceed Partial unless the expression contribution has been explicitly separated.
- Do not infer personality or morality from sex, age, ethnicity, or identity.
- Do not assign Strong applicability when the face is too small, heavily occluded, in extreme profile, or highly stylized.

## Applicability

- **Strong**: clear, low-context face with a neutral or mild expression; structural cues dominate.
- **Partial**: mild-to-moderate expression or pose is present, but structural impression still contributes independently.
- **Weak**: expression, context, or photographic style clearly competes; only a small correction is permitted.
- **Not applicable**: the face is unclear or social impression is not the main mechanism; final VA equals Direct.

## Reasoning Steps

1. Confirm face size, clarity, viewing angle, occlusion, and the strength of surrounding context.
2. Record dynamic actions in the brow-eye, mouth, and jaw regions separately, and first estimate the expression contribution.
3. If expression is strong, downgrade applicability; if it is mild, continue to relatively stable facial structure.
4. Cautiously estimate social valence from resting mouth configuration, brow-eye relations, facial maturity, width, and jaw structure.
5. Estimate perceived dominance from maturity, facial width, jaw structure, and head pose.
6. Combine these estimates with gaze direction to infer social approach, vigilance, or intimidation.
7. Check whether lighting, camera geometry, pose, or demographic bias could create a false impression.
8. Derive Valence from social valence and Arousal from the combination of dominance, direct gaze, and threat; then shrink the estimate toward Direct according to applicability.

## VA Mapping

| Visible state | Valence | Arousal |
|---|---:|---:|
| Warm, approachable, low-to-moderate dominance | 6.8-9.0 | 3.8-6.3 |
| Warm with authority or relatively high dominance | 6.3-8.7 | 5.5-7.8 |
| Low social valence, high dominance, direct intimidation | 3.0-5.0 | 6.6-9.1 |
| Unclear structural impression or competing expression/context | 4.8-6.2 | 4.5-6.5 |

## Direct-Anchor Rule

- First derive the skill-specific `skill_candidate`, then compute `final = direct + w x (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower applicability must produce a final estimate closer to Direct.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25. Extreme scores require both strong applicability and multiple converging cues.

## Boundary Notes

- Todorov evaluation concerns perceived first impressions, not personality recognition; the ethical limitation must appear in the result.
- This skill is especially vulnerable to expression and context contamination, so Partial or Weak cases must rely heavily on Direct.

## Output Format

Return fixed JSON reporting face quality, expression gating, structural cues, perceived social valence, perceived dominance, bias warnings, Direct inputs, candidate VA, weight, and final VA.
