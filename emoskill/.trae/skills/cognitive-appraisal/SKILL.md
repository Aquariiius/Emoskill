---
name: "cognitive-appraisal"
description: "Analyzes images using cognitive appraisal theory (Lazarus, Scherer, Smith & Ellsworth) to explain emotion as a function of inferred goal relevance, agency/responsibility, coping potential, and certainty — not just visible expression — then maps the resulting emotion hypotheses into valence-arousal space. Use specifically when the same visible cues (expression, posture, scene) are compatible with more than one plausible emotion, and resolving between them requires inferring the situation: who is responsible, what's at stake, whether the person can cope or control the outcome, why something is happening. Do NOT use when a discrete emotion is already clearly legible from expression/posture alone with no real ambiguity — use PANAS instead. Do NOT use for pure structural face-impression tasks (Todorov), restorative environment scenes (Kaplan), or aesthetic/compositional affect (Berlyne)."
---

# Cognitive Appraisal

## Purpose

Explain emotion in an image through the appraisal of the depicted situation — not just the visible expression — because appraisal theory's central finding is that identical cues can produce different emotions depending on inferred goals, responsibility, and coping potential. This skill exists specifically for the cases where that disambiguation is necessary: where context changes, or is needed to determine, the emotional read.

## Core Concepts

Drawing on Lazarus's primary/secondary appraisal structure and Smith & Ellsworth's dimensional model, use this compact set:

- **Goal relevance** — does this situation matter to the depicted person's apparent goals/well-being, or is it neutral background?
- **Goal congruence** — does the situation appear to help or threaten those goals?
- **Agency / responsibility** — who or what caused this (self, another person, circumstance)? Is the depicted person acting or being acted upon?
- **Coping potential / control** — does the person appear able to influence or manage the situation, or does it look beyond their control?
- **Certainty** — does the outcome look resolved, or ambiguous/unfolding?
- **Normative significance** (use when relevant) — does the situation involve a violation or fulfillment of social/moral expectations (e.g., unfairness, achievement)?

## Use When

Invoke this skill specifically when:

- Visible expression/posture alone is **ambiguous** or **compatible with multiple emotions**, and situational cues (setting, action, relationships, apparent stakes) are needed to disambiguate.
- The scene depicts stress, threat, achievement, frustration, embarrassment, guilt, or similar **context-dependent** emotions where the "why" materially changes the likely feeling (e.g., a person alone in an empty room could be lonely, relieved, or peacefully at rest — context decides).
- The task explicitly asks *why* an emotion might arise, not just what it is.
- A confident single-label read would be premature without considering agency, responsibility, or coping potential visible in the scene.

## Do-Not-Use-When Rules

Do not use this skill when:

- A **discrete emotion is already clearly legible** from face/posture/action with little real ambiguity (e.g., an unambiguous wide smile at a party, an unambiguous cry of distress) → use **PANAS** instead; appraisal reasoning adds little when there's nothing to disambiguate.
- The image is a **face-dominant, neutral-to-mildly-expressive portrait** where the read comes from facial structure rather than situation → defer to **Todorov**.
- The scene's affect is primarily about a **restorative natural/spatial environment** rather than a person's situational emotion → defer to **Kaplan**.
- The affect is driven by **composition, novelty, or aesthetic stimulation** rather than narrative/situational content → defer to **Berlyne**.

## Routing / Self-Check

Before proceeding, ask:

1. **Is there already a confident, unambiguous discrete-emotion read from visible cues alone?** If yes and context wouldn't change it → stop, note that PANAS is the better fit.
2. **Is the affect actually about environment or aesthetics, not a person's situational emotion?** If yes → defer to Kaplan or Berlyne.
3. **Is a face the dominant subject with a neutral/mild expression, where the point is structural impression rather than situation?** If yes → defer to Todorov.
4. If none of the above, and the emotional read genuinely depends on inferring goals, agency, responsibility, or coping potential → proceed.

State which check applied in the output.

## Reasoning Steps

1. **Self-check routing** — confirm appraisal reasoning is actually needed (see above); if not, name the better-fitting skill instead of proceeding.
2. Describe the likely situation and social context from visible evidence only (setting, actions, relationships, apparent stakes) — no invented backstory.
3. Infer appraisal dimensions (goal relevance, congruence, agency/responsibility, coping potential, certainty, normative significance) from what's visible, explicitly noting which are well-supported and which are speculative.
4. Generate **at least two competing emotion hypotheses** tied to different plausible appraisal readings of the same scene (this reflects the theory's core mechanism — same cues, different appraisal, different emotion) and state which is more likely and why.
5. Translate the leading hypothesis (and, if genuinely close, the runner-up) into a VA tendency — a range or a primary estimate with a noted alternative, rather than false precision.
6. Explicitly separate observation (what's visible) from interpretation (what's inferred), and flag what additional context would resolve the ambiguity.

## Output Format

```
ROUTING CHECK: [why appraisal reasoning is needed here rather than a sibling skill]
SITUATION SUMMARY: [observable scene/context, no invented backstory]
APPRAISAL DIMENSIONS: [goal relevance / congruence / agency-responsibility / coping potential / certainty / normative significance — each with supporting visible evidence]
COMPETING EMOTION HYPOTHESES: [2+ plausible emotions tied to different appraisal readings, ranked by likelihood]
VA TENDENCY: [valence + arousal estimate, noting range/alternate if hypotheses diverge]
OBSERVATION VS. INTERPRETATION: [explicit split of what's seen vs. inferred]
UNCERTAINTY / MISSING CONTEXT: [what information would change the read]
ETHICAL NOTE: [this is a scenario-based hypothesis about a depicted situation, not a factual claim about any real individual's actual thoughts, intentions, or responsibility]
```

## Uncertainty and Ethical Constraints

Appraisal reasoning inherently involves inferring goals, blame, and mental state — treat all such inferences as **plausible scenario hypotheses**, never as factual claims about a real, identifiable person's actual psychology, culpability, or intentions. Do not assign real-world blame or responsibility to any identifiable individual based on an image; frame agency/responsibility judgments in terms of what the *scene appears to depict*, not who is really at fault. If the subject is a recognizable public figure, keep interpretation strictly at the level of "a viewer might read this situation as..." Widen uncertainty rather than resolving ambiguity confidently when the image provides too little context to distinguish between competing appraisals.

## Examples That Should Trigger

- A person sitting alone in a hospital waiting room, expression neutral — is this dread, boredom, or relief? (context-dependent)
- Someone receiving a piece of paper from an official-looking figure, face partially unreadable — achievement or bad news? Needs situational cues.
- A person mid-argument with crossed arms — anger, defensiveness, or anxiety depend on inferred agency/blame.

## Examples That Should NOT Trigger

- Someone laughing uproariously at a party (unambiguous) → PANAS.
- A calm, neutral corporate headshot → Todorov.
- A misty forest trail with soft light → Kaplan.
- A boldly abstract, colorful mural → Berlyne.

## Ambiguous Cases

- **Person + expressive face + rich context:** if the expression alone is already decisive, use PANAS and mention context only as color; if context plausibly overturns the naive expression-based read (e.g., a "smiling" face in a context suggesting a forced or nervous smile), use Appraisal.
- **Group scenes with mixed apparent emotions:** describe the dominant or most narratively central figure's appraisal pattern, and note if multiple divergent appraisals coexist across figures.
- **Insufficient context to appraise:** if the scene gives almost no situational information beyond a face, say so explicitly and prefer PANAS or Todorov, rather than fabricating a scenario to justify using this skill.
