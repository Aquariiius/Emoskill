---
name: "todorov-face-evaluation"
description: "Optional non-VA feature module for explicit social-impression analysis of a clear neutral or mildly expressive face using Oosterhof and Todorov's perceived trustworthiness and dominance dimensions. It is excluded from the main affect router. Do not infer personality, intent, morality, competence, or final viewer valence-arousal."
---

# Todorov Face Evaluation

## Applicability Gate

REQUIRED:
- A clear human face is the dominant subject and surrounding event context is minimal.
- Expression is neutral, resting, or mild enough that structural first impression remains relevant.
- The user explicitly requests social-impression features rather than viewer VA or emotion recognition.

REJECT:
- Strong smile, crying, anger, fear, touch, conflict, intimacy, or situational action drives interpretation.
- Body posture, baby schema, occlusion, stylization, or surrounding context dominates.
- The task asks for actual character, intent, trustworthiness, danger, competence, diagnosis, or viewer VA.

NEAR MISS:
- Context-dependent face scene -> cognitive-appraisal.
- Whole-body action signal -> emotional-body-language.
- Infantile morphology -> baby-schema.

## Visual Variables

- **Face dominance/visibility**: size in frame, occlusion, resolution, angle, and lighting.
- **Expression strength**: neutral/resting versus clear affective expression.
- **Warmth/threat resemblance**: visible brow, eye-region tension, and resting mouth configuration, described without personality claims.
- **Dominance resemblance**: facial maturity, width, jaw prominence, and pose, treated as perceived structure rather than capacity.
- **Context contamination**: clothing, setting, interaction, identity cues, and stereotypes that may bias impression.
- **Reliability limits**: image quality, stylization, demographic bias, and mismatch between appearance and actual person.

## Inference Procedure

1. Confirm explicit use, face dominance, visibility, low context, and neutral/mild expression.
2. Record structural observations before using social-evaluation terms.
3. Estimate perceived trustworthiness/valence resemblance and cite the visible basis.
4. Estimate perceived dominance resemblance separately; do not convert either dimension into personality or intent.
5. Report uncertainty and bias limitations. Stop without producing final viewer VA.

## Feature Judgment

Return low, medium, or high perceived trustworthiness/valence resemblance and dominance resemblance with confidence. These are appearance-based first-impression features, not properties of the person. Strong expression or event context invalidates structural interpretation rather than becoming a modifier. Never translate the features into final valence-arousal scores.

## Worked Example

- **Image**: A well-lit, front-facing adult headshot with a closed resting mouth, relaxed brow, and plain background.
- **Analysis**: face visibility and low context are strong; expression is mild. Structural cues may support a tentative warmth and moderate-dominance impression, but identity and character remain unknowable.
- **Output**: perceived trustworthiness/valence resemblance = medium-high; perceived dominance resemblance = medium; uncertainty = medium because appearance judgments are bias-prone. No viewer VA is returned.

## Output Contract

Return `applicability`, `visual_evidence`, `perceived_trustworthiness`, `perceived_dominance`, `uncertainty`, and `ethical_limit`. Do not return final `valence_score` or `arousal_score`.
