---
name: "cognitive-appraisal"
description: "Analyze viewer affect from a visible event only when consequences or stakes and at least two appraisal dimensions have direct evidence. Separate observation from interpretation, compare hypotheses, and pass an evidence gate. This is not a default fallback; reject face-only, routine, and purely symbolic scenes."
---

# Cognitive Appraisal

## Applicability Gate

REQUIRED:
- A visible event, interaction, consequential object, or outcome determines affect rather than mere scene meaning.
- A visible gain/loss, obstruction, threat, success/failure, or consequential change makes the event relevant to a typical viewer; merely obtaining food/service or participating socially is not a stake.
- At least two appraisal dimensions have independent visible support.

REJECT:
- A direct mechanism dominates: restoration, perceptual stimulation, vastness, threat animal, contamination, baby schema, facial expression, or readable body action.
- The image is an ordinary object, face-only portrait, routine commerce/food service/social gathering, static symbol/memorial, or low-context scene without an unfolding event and consequential change.
- The interpretation requires invented history, dialogue, intention, consent, guilt, or personality.

NEAR MISS:
- Clear facial expression -> facial-expression-affect; clear posture with an unreadable face -> emotional-body-language.
- Safe infantile morphology -> baby-schema; visible danger may activate appraisal.
- Static solemn or symbolic meaning without a visible event -> no_specialized_skill.

ROUTING PRIORITY:
- Test direct mechanisms first. Appraisal is never the catch-all: ordinary goals such as buying, eating, waiting, or socializing do not count as stakes; with no consequential change or fewer than two supported dimensions, return `no_specialized_skill`.

## Visual Variables

- **Observation ledger**: visible people, objects, actions, contact, setting, and consequences; no mental states.
- **Viewer relevance**: why the visible event, rather than a depicted actor's private goal, affects a typical viewer.
- **Goal congruence**: evidence that the event helps, blocks, or threatens a plausible visible goal.
- **Agency/responsibility**: who visibly acts, controls an object, initiates contact, or receives consequences.
- **Coping/control**: escape routes, barriers, assistance, restraint, resources, or helpless positioning.
- **Certainty/imminence**: completed versus unfolding/ambiguous event; distance and time-to-impact cues.
- **Evidence status**: supported, contradicted, or unknown; missing context is never negative evidence.

## Inference Procedure

1. Build the observation ledger using only visible facts; remove emotion labels and unobserved intentions.
2. Represent actor-action-object/consequence relations, identify visible stakes, and state viewer relevance.
3. Generate two plausible situational hypotheses when ambiguity is real; state what evidence would distinguish them.
4. Estimate only supported appraisal dimensions and attach one observation to every estimate.
5. Apply the gate, then judge valence from visible congruence and arousal from urgency, imminence, and coping demand. Strong requires an event, a stake, and two supported dimensions; otherwise reject or widen uncertainty.

## VA Judgment

Use the shared 1-9 scale without a lookup table. Visible goal incongruence lowers valence; congruence raises it. Arousal rises with an unfolding event, imminent consequence, demonstrated low control, or unresolved consequential uncertainty. Static symbolism, completed outcomes, solemn meaning, and absent exits/help do not establish urgency. Report viewer affect, not a depicted actor's private state.

## Worked Example

- **Image**: A damaged car blocks a road; one person stands with hands on head, another approaches, and smoke is visible, but no injury is shown.
- **Analysis**: blocked travel, smoke, loss of control, and possible assistance threaten safety, but coping may be available; hypotheses are manageable accident versus escalating danger.
- **VA**: valence 3.2, arousal 6.3 on 1-9; partial-to-strong applicability, with uncertainty from unseen injuries and outcome.

## Output Contract

Include the observation ledger, visible event and stakes, viewer relevance, supported dimensions, competing hypotheses, and gate decision. Treat unsupported dimensions as unknown, never as evidence.
