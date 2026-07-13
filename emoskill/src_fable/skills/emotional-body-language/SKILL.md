---
name: "emotional-body-language"
description: "Analyze perceived affect from human whole/upper-body configuration when posture, tension, orientation, and action readiness are primary and the face is unreadable or secondary. Classify the action context first: recreation/sport/dance and celebration are POSITIVE action, not conflict. Do not use when object meaning, facial expression, or situational stakes carry affect."
---

# Emotional Body Language

## Applicability Gate

REQUIRED:
- A human whole body or visible upper body carries the main emotional signal.
- Face information is absent, obscured, too small, masked, or secondary.
- Posture supports a recognizable action tendency: approach, recoil, freeze, attack, collapse, celebrate, assert, submit.

REJECT:
- A readable face or facial expression dominates -> facial-expression-affect.
- A weapon, risky object, or consequence determines affect -> cognitive-appraisal.
- Only an isolated hand, ambiguous resting pose, or small fragment is visible.

NEAR MISS:
- Visible agency, stakes, conflict, or object use -> cognitive-appraisal.
- Neutral face-centered portrait -> no specialized skill.
- Predatory animal posture -> evolved-fear-module.

## Visual Variables

- **Action context (FIRST)**: sport, dance, recreation, celebration, labor, protest, violence, or unclear — this sets the valence branch.
- **Expansion/contraction**: open versus closed torso, raised versus tucked or shielding limbs.
- **Tension/energy**: rigid joints, muscular loading, explosive motion, slackness, collapse.
- **Orientation**: forward lean, recoil, turning away, upward extension, grounded stance.
- **Victim/threat check**: any person being harmed, fleeing, or dominated flips the branch negative.

## Inference Procedure

1. Verify body visibility; apply the removal test (would the signal survive hiding the face?).
2. Classify the action context BEFORE reading emotion; sport/dance/play frames are positive-action unless a victim, weapon, or collision harm is visible.
3. Describe configuration (expansion, tension, orientation) without naming an emotion.
4. Infer primary and one competing action tendency; static frames can mimic emotion.
5. Judge VA with the anchors; arousal follows postural energy, not the emotion label.

## Arousal Gate

Arousal follows VISIBLE energy: explosive motion, rigid loading, mid-air phases, or full sprint
raise it; standing, walking, posing, or slack postures do not. A dramatic mood without motion
is NOT an activation cue. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Case | Valence | Arousal |
|---|---:|---:|
| Celebration, sport, dance, energetic play (no victim) | 6.5-7.6 | 5.4-6.6 |
| Aggression or attack posture toward someone | 2.5-3.5 | 6.0-7.2 |
| Fear: recoil, shielding, fleeing | 3.0-4.0 | 5.5-6.5 |
| Sadness: collapse, slumped withdrawal | 2.8-3.8 | 3.0-4.4 |
| Calm neutral activity or ambiguous pose | 5.0-6.0 | 3.4-4.5 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Positive action**: A runner crosses a finish line, arms raised high, back arched, mid-stride.
  -> sport context, expansion, explosive motion, no victim; activation_evidence ["sprint
  motion", "arms thrust upward"]. **V 7.2, A 6.2**, strong.
- **Sad**: A lone figure sits slumped on a curb, head down, shoulders collapsed, motionless. ->
  contraction, slackness, withdrawal, no motion; activation_evidence []. **V 3.2, A 3.6**,
  strong.

## Output Contract

In the shared JSON report action context, body configuration before interpretation, competing
tendencies, and top-level `activation_evidence` (empty list if none). Describe perceived
expression, not actual inner state.
