---
name: "emotional-body-language"
description: "Analyzes how posture, gesture, muscle tension, center of mass, orientation, and action readiness create perceived body emotion. Use only when the body signal survives a face-occlusion test."
---

# Emotional Body Language
## Purpose
Infer action readiness and activation from visible body configuration without treating a static pose as the person's true internal emotional state.
## Routing Card
USE WHEN:
- Whole-body or upper-body posture is the primary affective carrier and the face is absent, unreadable, or secondary.
- Torso, limbs, center of mass, and tension jointly support approach, withdrawal, attack, freezing, or celebration.
DO NOT USE WHEN:
- Meaning depends mainly on a weapon, interaction partner, social relation, or event consequence.
- Readable facial action clearly dominates whole-image affect.
VISUAL TRIGGERS:
- Contraction, shielding, leaning back, lunging, rigidity, collapse, raised arms, jumping, clenched fists.
- Forward or backward center of mass, spatial expansion or contraction, and visible motion continuation.
NEAR-MISS BOUNDARIES:
- Objects and consequences determine posture meaning -> `cognitive-appraisal`.
- Neutral or mildly expressive facial structure dominates -> `todorov-face-evaluation`.

## Core Constructs
- **Expansion–contraction**: open limbs and occupied space versus protective inward reduction.
- **Tension and movement energy**: rigidity, gripping, joint flexion, speed cues, and imbalance.
- **Center of mass and orientation**: forward approach, backward retreat, turning away, downward collapse, or upward extension.
- **Action readiness**: attack, flee, freeze, approach, celebrate, submit, soothe, or recover.

## Use When
Apply the face-occlusion test: Strong fit requires the same main action tendency to remain after all facial information is hidden.
## Do-Not-Use-When Rules
- Do not infer whole-person emotion from one hand or a small body fragment.
- Sports, dance, and transitional frames require explicit motion-phase uncertainty.
- Describe perceived body expression only; do not infer personality, power, or true intent.

## Applicability
- **Strong**: torso, limbs, and center-of-mass cues converge in direction.
- **Partial**: body evidence is clear but objects, face, or context competes.
- **Weak**: only fragments, posed posture, or a transitional action frame is visible.
- **Not applicable**: the interpretation fails after face occlusion; final VA equals Direct.

## Reasoning Steps
1. Perform the face-occlusion test and confirm that the body independently carries affect.
2. Describe torso openness, shoulders, arms, legs, joint angles, and occupied space.
3. Assess muscle tension, center-of-mass stability, orientation, and motion continuation.
4. Map configuration to concrete action readiness before applying emotion labels.
5. Check whether interaction objects, weapons, sport rules, or dance context changes meaning.
6. Generate two action hypotheses, such as aggressive lunge versus athletic sprint, and compare evidence.
7. Derive Valence from approach or withdrawal direction and outcome; derive Arousal from tension, speed, and imbalance.
8. Set applicability from body-signal independence and anchor fragmentary or ambiguous poses to Direct.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Shielding, leaning back, contraction, freezing | 2.4–4.4 | 6.4–9.1 |
| Forward lunge, clenched fists, attack readiness | 2.7–4.9 | 7.2–9.8 |
| Drooping, slumped shoulders, low movement energy | 3.0–4.6 | 2.7–5.3 |
| Raised arms, jumping, stable celebration | 7.8–10.0 | 6.4–9.1 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- Body language describes what the body appears ready to do, not a diagnosis of true emotion.
- When an object or event determines meaning, lower fit and give Direct or cognitive appraisal more weight.

## Worked Example
A person leans back with both arms shielding the chest and knees bent: contraction, shielding, and backward center of mass support defensive withdrawal. A visible ball and sports court would strengthen a catching hypothesis and reduce fit.

## Output Format
Return fixed JSON with the face-occlusion test, body configuration, action readiness, competing interpretation, Direct inputs, candidate VA, blend weight, and final VA.
