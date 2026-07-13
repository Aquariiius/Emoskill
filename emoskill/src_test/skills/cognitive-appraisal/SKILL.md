---
name: "cognitive-appraisal"
description: "Analyzes context-dependent VA through visible goal relevance, goal congruence, agency, control, certainty, and normative significance. Use when event meaning, rather than a single specialized cue, dominates."
---

# Cognitive Appraisal
## Purpose
Explain why the viewer reacts to what is happening and what it means for affected actors. Visible facts must be separated from interpretation, and strong conclusions require competing hypotheses and an evidence gate.
## Routing Card
USE WHEN:
- Actors, actions, objects, affected parties, or visible outcomes can be identified.
- The same face, posture, or object changes meaning only after goals, responsibility, and consequences are interpreted.
DO NOT USE WHEN:
- Contamination, animal attack morphology, baby schema, physical vastness, or restoration already explains VA.
- No visible stakes exist and the explanation depends on scene labels or invented backstory.
VISUAL TRIGGERS:
- Conflict, helping, failure, success, intimacy, exclusion, accidents, weapon use, responsibility, and consequences.
- Actions visibly change safety, affiliation, achievement, dignity, or resource conditions.
NEAR-MISS BOUNDARIES:
- The body independently conveys action readiness -> `emotional-body-language`.
- A neutral or mildly expressive face is evaluated structurally -> `todorov-face-evaluation`.

## Core Constructs
- **Goal relevance and congruence**: whether an important goal is involved and is being helped or obstructed.
- **Agency and affected party**: who acts, who benefits or suffers, and whether the act appears intentional.
- **Control and coping**: whether actors can stop, escape, repair, or obtain the outcome.
- **Certainty, urgency, and normative meaning**: how soon and clearly the outcome develops and whether fairness, duty, or taboo is visible.

## Use When
Use when removing key relations and event objects would make facial or bodily cues insufficient to explain the whole-image affect.
## Do-Not-Use-When Rules
- Do not invent history, identity, motives, or outcomes outside the frame.
- Do not infer consent from an embrace or a cause from crying alone.
- Mark Not applicable when no visible goal, agency, or consequence exists.

## Applicability
- **Strong**: at least three of actor, action, affected party, and outcome are clear.
- **Partial**: the event is visible but intention, responsibility, or outcome has competing interpretations.
- **Weak**: stakes are only suggested by a scene category or one object.
- **Not applicable**: event structure is absent; final VA equals Direct.

## Reasoning Steps
1. Record actors, actions, objects, affected parties, setting, and visible outcomes.
2. Separate observations from interpretations and remove claims without a visual referent.
3. Identify the most immediate safety, affiliation, achievement, dignity, or resource goal.
4. Determine whether the goal is helped or blocked and who may cause or bear the outcome.
5. Assess control, outcome certainty, temporal urgency, and normative significance.
6. Generate at least two plausible affective hypotheses with supporting and contradicting evidence.
7. Select the hypothesis with broader evidence coverage and infer approach, helping, defense, or withdrawal.
8. Derive Valence from benefit or harm and Arousal from urgency, uncertainty, and low control, then blend with Direct according to fit.

## VA Mapping
| Visible state | Valence | Arousal |
|---|---:|---:|
| Clear harm with low control | 1.6–3.5 | 7.8–10.0 |
| Developing risk with uncertain outcome | 3.0–4.9 | 6.4–8.9 |
| Clear help, success, or safe affiliation | 7.5–9.8 | 4.6–8.0 |
| Competing event meanings with limited evidence | 4.7–6.3 | 4.2–6.6 |

## Direct-Anchor Rule
- First estimate the skill-specific `skill_candidate`, then compute `final = direct + w × (skill_candidate - direct)`.
- Use fixed weights: `strong=0.85`, `partial=0.55`, `weak=0.25`, and `not_applicable=0`; lower fit must remain closer to Direct VA.
- If evidence supports only Valence or only Arousal, the unsupported dimension must use a weight no greater than 0.25; extreme scores require strong fit and multiple convergent cues.
## Boundary Notes
- This skill handles event meaning, not strong emotion from face, posture, or object category alone.
- Low fit must be expressed through a smaller blend weight, not merely mentioned as verbal uncertainty.

## Worked Example
One person helps another person up: the helping action promotes recovery and raises coping potential, but the image does not prove a severe accident. The candidate is positive with moderate arousal; unclear cause or relationship requires Partial fit and a result closer to Direct.

## Output Format
Return fixed JSON with factual observations, appraisal dimensions, at least one alternative hypothesis, Direct inputs, candidate VA, applicability weight, final VA, and confidence.
