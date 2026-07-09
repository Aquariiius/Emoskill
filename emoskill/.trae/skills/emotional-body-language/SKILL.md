---
name: "emotional-body-language"
description: "Analyzes affect from human body posture, gesture, and action readiness when the face is absent, unreadable, or secondary. It maps expansion/contraction, tension, orientation, energy, and action tendency into valence-arousal. Do not use when facial expression, situational stakes, or object threat is the main affective source."
---

# Emotional Body Language

## Purpose

Estimate affect from visible human body configuration: posture, gesture, tension, orientation, expansion, contraction, and implied action readiness. This skill is for body-carried emotion, not facial expression or object-based threat.

## Routing Card

USE WHEN:
- Body posture, gesture, or whole-body/upper-body configuration is the primary emotional signal.
- Face is absent, obscured, too small, masked, or secondary.
- Affect comes from action readiness: freeze, flee, approach, attack, collapse, expand, contract, assert, submit.

DO NOT USE WHEN:
- A readable face is dominant.
- The main affective cue is an object or weapon being used rather than body configuration.
- Situational agency/context, baby schema, animal threat, contamination, restoration, aesthetics, or vastness is stronger.

VISUAL TRIGGERS:
- Contracted/shielding body, recoil, forward lean, clenched limbs, slumped collapse, expanded triumph, dominant stance.
- Silhouettes, crowds, dance, protest, sport/action freeze-frames with unreadable faces.
- Whole-body or upper-body action readiness, not isolated hands alone.

NEAR-MISS BOUNDARIES:
- Weapon aimed or risky object use -> cognitive-appraisal unless whole-body posture is primary.
- Neutral or mild face-dominant image -> todorov-face-evaluation.
- Animal predatory posture -> evolved-fear-module.

## Core Constructs

- **Expansion vs. contraction**: open/large postures often imply dominance, joy, approach; closed/small postures imply fear, submission, withdrawal.
- **Postural energy**: tension, rigidity, motion, and force drive arousal.
- **Orientation**: forward approach, turning away, recoil, collapse, or upward extension changes affect.
- **Action readiness**: the posture prepares for fight, flee, freeze, approach, celebrate, withdraw, assert, or appease.
- **Gaze modifier**: direct gaze may raise arousal only when posture remains the main signal.

## Use When

Use this skill when the body itself communicates the emotional payload. It should still work if the face is removed from the image.

## Do-Not-Use-When Rules

- Do not use for isolated hand/object threats where the object carries meaning.
- Do not use for clear face expression or structural face impression.
- Do not use if posture is ambiguous and context is needed to decide; use Cognitive Appraisal.
- Do not infer actual inner state; report perceived body expression.

## Applicability

Strong:
- Whole-body or upper-body posture clearly conveys action readiness.

Partial:
- Body cues are present but compete with face, object, or context.

Weak:
- Only small body fragments or ambiguous static pose are visible; keep VA conservative.

## Reasoning Steps

1. Confirm body configuration is the primary emotional signal.
2. Describe expansion/contraction, tension, orientation, limb position, and motion cues.
3. Map posture to action readiness.
4. Estimate postural energy for arousal.
5. Apply gaze modifier only if visible and secondary.
6. Map perceived body expression to VA with uncertainty.

## VA Mapping

| Body Pattern | Valence | Arousal |
|---|---:|---:|
| Fear/recoil/shielding/freezing | 2.0-4.0 | 6.0-8.5 |
| Anger/aggressive forward action | 2.5-4.5 | 6.5-9.0 |
| Sadness/collapse/withdrawal | 2.5-4.0 | 2.5-5.0 |
| Joy/triumph/open celebration | 7.5-9.2 | 6.0-8.5 |
| Dominance/assertive stance | 5.0-7.0 | 5.5-7.5 |
| Weak body evidence | keep near direct VA | keep conservative |

## Boundary Notes

- Body Language is not a general "human present" skill.
- Object meaning can dominate posture; if stakes/agency matter, use Cognitive Appraisal.
- Static images can misread motion; widen uncertainty for dance, sport, or transitional poses.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report body configuration, action readiness, postural energy, boundary checks, and VA mapping.
