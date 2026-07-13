---
name: "emotional-body-language"
description: "Analyze perceived affect from human whole/upper-body configuration when posture, tension, orientation, and action readiness are primary and the face is unreadable or secondary. Progress from body visibility through configuration, energy, and action tendency before VA. Do not use when object meaning, facial expression, or situational stakes carry affect."
---

# Emotional Body Language

## Applicability Gate

REQUIRED:
- A human whole body or sufficiently visible upper body carries the main emotional signal.
- Face information is absent, obscured, too small, masked, or secondary.
- Posture supports a recognizable action tendency such as approach, recoil, freeze, attack, collapse, celebration, assertion, or submission.

REJECT:
- A readable facial expression dominates -> facial-expression-affect.
- A weapon, risky object, interaction, or consequence determines affect more than body configuration.
- Only an isolated hand, ambiguous resting pose, or small body fragment is visible.

NEAR MISS:
- Clear expressive face -> facial-expression-affect; a neutral face-centered portrait -> no_specialized_skill.
- Visible agency, stakes, conflict, or consequential object use -> cognitive-appraisal.
- Predatory animal posture -> evolved-fear-module.

## Visual Variables

- **Body visibility**: whole/upper-body coverage, occlusion, angle, and reliability of joint configuration.
- **Expansion/contraction**: open versus closed torso, occupied space, raised versus tucked limbs, protective covering.
- **Tension/energy**: rigid joints, clenched limbs, muscular loading, slackness, collapse, or visible force; blur alone is unreliable.
- **Orientation**: forward lean, recoil, turning away, upward extension, crouch, retreat, or grounded stance.
- **Limb configuration**: shielding, reaching, striking, embracing, bracing, celebrating, or hanging loosely.
- **Action readiness**: approach, fight, flee, freeze, withdraw, submit, assert, celebrate, or seek support.
- **Modifiers**: gaze direction, crowd synchrony, sport/dance context, transitional motion, and interaction objects.

## Inference Procedure

1. Verify body visibility and apply the removal test; lower applicability when face or object meaning is necessary.
2. Describe expansion, contraction, tension, orientation, and limb configuration without naming an emotion.
3. Infer one primary and, if needed, one competing action tendency from the configuration.
4. Estimate postural energy from tension, motion, loading, and collapse; do not use emotional category alone to set arousal.
5. Apply gaze, crowd, sport/dance, and transition modifiers, then judge VA from action tendency and energy; report ambiguity between similar poses.

## VA Judgment

Use the shared 1-9 scale without fixed ranges. Valence follows perceived approach/avoidance, not raw expansion/contraction; do not infer conflict, pain, or aggression without a visible target, contact, or consequence. Arousal follows reliable postural energy: rigid loading, explosive motion, recoil, or celebration can raise it; slack, standing, or resting posture lowers it. Motion blur and a single sport/dance frame are not sufficient evidence of high energy or threat. Distinguish the depicted expression from viewer affect.

## Worked Example

- **Image**: A distant person leans backward with shoulders raised, elbows bent, and both hands shielding the upper body; the face is too small to read and no weapon is visible.
- **Analysis**: contraction, recoil, upper-body tension, and little object context imply avoidance/protection with moderate-high energy; fear-like readiness is more plausible than sadness or rest.
- **VA**: valence 3.3, arousal 5.8 on 1-9; strong body-language applicability, with arousal kept below extreme because the trigger and actual motion are unseen.

## Output Contract

In the shared JSON, report body configuration before interpretation, competing action tendencies, energy reliability, and the distinction between depicted expression and viewer response. Describe perceived expression, not actual inner state.
