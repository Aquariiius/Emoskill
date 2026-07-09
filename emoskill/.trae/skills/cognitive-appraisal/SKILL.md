---
name: "cognitive-appraisal"
description: "Analyzes affect from inferred situation meaning using cognitive appraisal dimensions: goal relevance, goal congruence, agency/responsibility, coping potential/control, certainty, and normative significance. Use when visible stakes, responsibility, risk, social meaning, or context are needed to interpret affect. Do not use when a specialized visible mechanism is stronger."
---

# Cognitive Appraisal

## Purpose

Explain affect as a response to what the depicted situation appears to mean: what is at stake, who has agency, whether goals are helped or threatened, whether coping is possible, and how certain the outcome is. This skill is for context-dependent emotion, not generic emotion labeling.

## Routing Card

USE WHEN:
- Affect depends on inferred goals, stakes, agency, responsibility, coping, certainty, or social norms.
- Visible action or context changes the emotional meaning of the same face, posture, or object.
- Human risk, conflict, intimacy, achievement, failure, norm violation, or non-animal danger requires interpretation.

DO NOT USE WHEN:
- Whole-body posture alone clearly carries the emotion.
- A neutral or mildly expressive face is the dominant structural cue.
- Restoration, aesthetic stimulation, physical vastness, contamination, baby schema, or threat animal is the stronger visible mechanism.

VISUAL TRIGGERS:
- Weapons, risky behavior, social interaction, vulnerability, conflict, authority, achievement/failure, ambiguous touch, visible consequences.
- Human-centered scenes where "what is happening and why it matters" determines affect.
- Strong stakes without a fear-relevant animal or pathogen cue.

NEAR-MISS BOUNDARIES:
- Isolated weapon or risky object use -> cognitive-appraisal if agency/stakes matter.
- Clear whole-body action readiness -> emotional-body-language.
- Neutral portrait with little context -> todorov-face-evaluation.

## Core Concepts

- **Goal relevance**: does the event matter to safety, affiliation, achievement, dignity, or well-being?
- **Goal congruence**: does it help or threaten those goals?
- **Agency/responsibility**: who appears to act, cause, choose, or be affected?
- **Coping potential/control**: is the situation manageable or uncontrollable?
- **Certainty**: is the outcome clear, unfolding, or ambiguous?
- **Normative significance**: are rules, duties, taboo, fairness, or social expectations involved?

## Use When

Use this skill when visible evidence supports more than a surface label. The image should require situational interpretation, not simply "person smiles" or "person stands".

## Do-Not-Use-When Rules

- Do not infer strong pleasure, consent, guilt, regret, or excitement from scene category alone.
- Do not use when face structure, body posture, animal threat, contamination, restoration, aesthetics, or vastness is clearly primary.
- Do not invent backstory; separate observation from interpretation.
- If no stakes or appraisal dimensions are visible, route to `no_specialized_skill` or another better fit.

## Applicability

Strong:
- Visible stakes and agency clearly shape affect.

Partial:
- Context matters, but evidence for specific emotion is limited.

Weak:
- The scene category suggests emotion, but visible appraisal evidence is thin; keep VA conservative.

## Reasoning Steps

1. Identify visible situation, actors, actions, objects, and stakes.
2. Separate observations from interpretations.
3. Score appraisal dimensions from visible evidence only.
4. Generate at least two plausible emotion hypotheses when ambiguity is real.
5. Apply an evidence-strength gate before assigning strong VA.
6. Map the leading appraisal pattern to valence and arousal.

## VA Mapping

| Appraisal Pattern | Valence | Arousal |
|---|---:|---:|
| Clear threat, low control | 1.5-3.5 | 7.0-10.0 |
| Risk/norm violation, uncertain outcome | 2.5-4.5 | 5.5-8.0 |
| Positive goal congruence, active engagement | 6.5-8.5 | 5.5-8.0 |
| Safe intimacy or affiliation, well-supported | 7.0-9.0 | 4.5-7.5 |
| Ambiguous or weak evidence | 4.5-6.5 | 4.0-6.5 |

## Boundary Notes

- Appraisal can handle obvious danger if the affect comes from agency, stakes, and control.
- It should not over-mentalize pleasant categories without visible support.
- For guns, vehicles, violations, and social stakes, this skill is often better than body-language if the object/action carries the threat.
- If no specialized cue strongly fits, route to `no_specialized_skill`.

## Output Format

The experiment prompt converts this analysis into JSON. Include top-level `valence_score`, `arousal_score`, and `applicability`. In the rationale, report observations, appraisal dimensions, competing hypotheses if needed, evidence strength, and VA mapping.
