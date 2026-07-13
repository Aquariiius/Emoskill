---
name: "cognitive-appraisal"
description: "Conditional event-appraisal skill for images where a VISIBLE consequential event (gain/loss, harm, obstruction, success, affiliation, violation) determines affect. Requires visible stakes plus two evidence-supported appraisal dimensions; it is NOT a fallback for people-present or ambiguous images. Positive events (affection, achievement, intimacy) are appraised with the same discipline as threats."
---

# Cognitive Appraisal

## Applicability Gate

REQUIRED:
- A visible consequential change or stake: harm, danger, loss, obstruction, rescue, achievement, affection, intimacy, or norm violation.
- Affect cannot be read from a single direct mechanism without interpreting the situation.
- At least two appraisal dimensions have independent visible evidence.

REJECT (route to no_specialized_skill, not here):
- People merely present, posing, standing, eating, shopping, working, or doing routine activity with no visible consequence.
- A direct mechanism dominates: face expression, body action, contamination, threat animal, baby schema, restoration, vastness, composition.
- The interpretation would require invented history, intention, consent, or personality.

NEAR MISS:
- Clear posture signal with little context dependence -> emotional-body-language.
- Readable expressive face -> facial-expression-affect.
- Weapon/accident/violence stays here when agency and consequences are visible.

## Visual Variables

- **Observation ledger**: visible people, objects, actions, contact, setting, consequences; no mental states.
- **Goal congruence**: the event visibly helps (affection, success, care) or harms (injury, loss, attack) someone.
- **Agency/control**: who acts, who is affected, escape or coping options.
- **Certainty/imminence**: unfolding versus completed; time-to-impact cues.
- **Event polarity check (MANDATORY)**: decide help-or-harm before scoring; embraces, kisses, celebrations, and rescue are POSITIVE events.

## Inference Procedure

1. Build the observation ledger from visible facts only.
2. State the consequential change. If you cannot name one, output applicability weak and defer.
3. Classify event polarity (positive / negative / ambiguous) with cited evidence.
4. Estimate only supported dimensions; give two hypotheses when ambiguity is real.
5. Judge VA with the branch anchors; unfolding danger is activating, aftermath is NOT.

## Arousal Gate

Arousal follows imminence and urgency, not severity of meaning: an unfolding attack is high;
a completed accident, grief scene, funeral, or aftermath photo is LOW-TO-MID (3.5-5.2). Sad or
serious meaning is NOT an activation cue. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Branch | Valence | Arousal |
|---|---:|---:|
| Unfolding attack/threat with weapon or violence | 2.0-3.0 | 6.0-7.5 |
| Aftermath: completed accident, loss, grief | 2.5-3.5 | 4.0-5.2 |
| Affiliation/care: embrace, comfort, family warmth | 6.5-7.5 | 4.2-5.4 |
| Intimacy/erotic couple, consensual framing | 6.5-7.5 | 5.4-6.4 |
| Achievement/celebration outcome | 6.5-7.5 | 5.0-6.0 |
| Ambiguous stakes (prefer deferring instead) | 4.5-5.5 | 4.0-5.0 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Negative**: A person aims a handgun at a cowering victim indoors. -> unfolding harm, clear
  agency, no escape visible; activation_evidence ["aimed weapon", "cowering victim"].
  **V 2.4, A 6.9**, strong.
- **Positive**: Two people embrace tightly at an airport arrival gate, luggage beside them. ->
  reunion event, affiliation gain, mutual approach; activation_evidence ["active embrace"].
  **V 7.2, A 5.0**, strong.

## Output Contract

Include the observation ledger, event polarity, supported dimensions, competing hypotheses, and
top-level `activation_evidence` (empty list if none). Never report invented intention as fact.
