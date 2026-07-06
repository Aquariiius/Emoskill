---
name: "panas-discrete-va"
description: "Matches images to PANAS discrete affect terms (Watson, Clark & Tellegen) and maps them to valence-arousal through an explicit mapping table. Use when a discrete emotion is clearly legible from visible cues (face, posture, gesture, action) with little real ambiguity, and especially when the affect is an activated/high-arousal state (excitement, distress, alertness, hostility, nervousness). Do NOT use when the emotion depends on inferring situational context, goals, or responsibility to resolve ambiguity — use Cognitive Appraisal instead. Do NOT use for calm, serene, bored, content, disgusted, or low-arousal affect, which PANAS's vocabulary does not cover well — consider Kaplan ART for calm/restorative scenes. Do NOT use for neutral-face structural impressions (Todorov) or aesthetic/compositional affect (Berlyne)."
---

# PANAS Discrete Emotion VA

## Purpose

Use this skill for image VA analysis when the emotion is already legible from visible cues and can be matched directly to one or more of the PANAS discrete affect terms (Watson, Clark & Tellegen, 1988), then converted to valence-arousal through an explicit mapping table. PANAS was built as a two-factor model of **activated** positive and negative affect: Positive Affect (PA) reflects the extent to which someone feels enthusiastic, active, and alert, and Negative Affect (NA) reflects general distress (anger, guilt, fear, and similar). Both dimensions are predominantly defined by the *activation* of valenced affect — the low end of each represents its **absence** (calm, flat) rather than a distinct opposite state such as serenity or contentment. This is the single most important thing to know about PANAS for image analysis: it is strong at describing energized, activated emotion, and structurally weak at describing calm, low-arousal, or affectively "flat/quiet" states.

## Core Concepts

- **PANAS positive affect terms:** interested, excited, strong, enthusiastic, proud, alert, inspired, determined, attentive, active
- **PANAS negative affect terms:** distressed, upset, guilty, scared, hostile, irritable, ashamed, nervous, jittery, afraid
- **Coverage gap:** PANAS's 20 terms do not include calm, content, serene, bored, disgusted, or peaceful. These affects are real and common in images but sit outside PANAS's vocabulary — do not force-fit them onto the nearest PANAS term.
- The core task is discrete affect matching from directly visible cues, followed by VA aggregation through an explicit mapping table — not situational inference (that's Cognitive Appraisal's job).

## Use When

Invoke this skill when:

- A discrete emotion is directly legible from face, posture, gesture, action, or immediate scene cues, with little real ambiguity about which emotion is present.
- The visible affect is plausibly an **activated/energized** state (excited, distressed, alert, hostile, nervous, enthusiastic) rather than a calm or low-arousal one.
- The task explicitly asks for a PANAS- or PANAS-style discrete-emotion-to-VA analysis.
- Situational context would not meaningfully change the emotional read (i.e., there's nothing to disambiguate).

## Do-Not-Use-When Rules

Do not use this skill when:

- The correct label depends on inferring **why** something is happening, who is responsible, or what's at stake — the visible cues alone are ambiguous or support multiple readings → defer to **Cognitive Appraisal**.
- The likely affect is calm, serene, content, peaceful, bored, or disgusted — states PANAS's vocabulary does not cover well → consider **Kaplan ART** (for calm/restorative environments) or note the coverage gap explicitly rather than forcing a PANAS label.
- The face is the dominant subject and neutral/mildly expressive, and the read is about structural social impression (trust, dominance) rather than an expressed emotion → defer to **Todorov**.
- The affect is driven by composition, novelty, or aesthetic stimulation rather than a person's expressed emotion → defer to **Berlyne**.

## Routing / Self-Check

Before proceeding:

1. **Is there a confident, directly-legible discrete emotion?** If it requires situational/contextual inference to resolve, stop and defer to Cognitive Appraisal.
2. **Does the likely affect fall within PANAS's activated-state vocabulary?** If the scene reads as calm, serene, bored, content, or disgusted, flag the coverage gap rather than forcing the nearest term, and consider whether Kaplan is the better fit.
3. **Is a face the dominant subject with a neutral/mild expression, driving a structural impression rather than an expressed emotion?** If so, defer to Todorov.
4. If none of the above apply, proceed with PANAS matching.

State which check applied in the output.

## Mapping Principle

- First infer 2 to 5 PANAS affect terms from visible evidence.
- Then assign normalized weights across the selected affect terms.
- Then use the configured PANAS emotion-to-VA mapping table.
- Finally aggregate the weighted coordinates into the final valence and arousal values.
- If the best-fitting PANAS terms are all weak matches (low confidence across the board), treat this as a signal of a coverage gap rather than picking the least-bad term with high confidence.

## Reasoning Steps

1. **Self-check routing** — confirm this is a directly-legible, activation-compatible discrete emotion case; if not, name the better-fitting skill instead of proceeding.
2. Identify visible cues from face, posture, gesture, action, and immediate scene context.
3. Select the most plausible PANAS affect terms supported directly by those cues.
4. Distinguish primary affect terms from weaker competing affect terms; explicitly note if all candidate terms are weak matches (coverage gap).
5. Assign normalized weights over the selected affect terms.
6. Aggregate the final VA estimate through the PANAS mapping table.
7. Explain ambiguity when the image supports multiple competing affect interpretations, and flag if situational context (rather than more visual cues) would be needed to resolve it — a sign Appraisal may have been the better fit.

## Output Format

```
ROUTING CHECK: [why PANAS matching is appropriate here, and which deferrals were ruled out]
OBSERVED VISUAL CUES: [face, posture, gesture, action, immediate context]
MATCHED PANAS AFFECT TERMS: [2-5 terms, ranked]
COVERAGE CHECK: [do the matched terms fit well, or is this a coverage gap — e.g., scene reads as calm/bored/disgusted/content]
NORMALIZED EMOTION WEIGHTS: [weights across selected terms]
MAPPING TRACE: [how weighted terms were aggregated to VA]
FINAL VALENCE: [value]
FINAL AROUSAL: [value]
UNCERTAINTY NOTES: [confidence, competing interpretations, coverage-gap flag if relevant]
```

## Uncertainty and Ethical Constraints

Treat matched affect terms as the *most plausible visible read*, not a certain diagnosis of what the depicted person is actually feeling — a person's true internal state cannot be confirmed from an image alone. Avoid overconfident claims when cues are subtle, mixed, or contradictory; widen uncertainty rather than forcing a confident single-term match. Do not use this skill to make claims about a real, identifiable individual's genuine emotional or mental state as fact — frame output as "the visible cues most closely match..." rather than "this person is feeling...".

## Examples That Should Trigger

- A sprinter crossing a finish line, arms raised, mouth open — clearly excited/proud.
- Someone visibly flinching with wide eyes at a sudden loud event — clearly scared/nervous.
- A crowd cheering with raised fists — clearly enthusiastic/excited.

## Examples That Should NOT Trigger

- A person staring blankly at a letter, expression unreadable — ambiguous, needs context → Cognitive Appraisal.
- A calm, neutral corporate headshot → Todorov.
- Someone lying peacefully in a hammock in a garden → Kaplan (PANAS has no good "peaceful/content" term).
- A wrinkled-nose reaction to a bad smell → note the coverage gap explicitly (disgust isn't a PANAS term) rather than mislabeling it as "distressed" or "upset."

## Ambiguous Cases

- **Mixed or conflicting cues** (e.g., tears during a joyful event): report competing PANAS terms with weights reflecting the ambiguity rather than picking one confidently, and note that Cognitive Appraisal may better resolve which is dominant.
- **Weak match across all candidate terms:** explicitly report this as a coverage gap (likely a calm/bored/disgusted/content state) rather than forcing the least-bad PANAS label.
- **Activated but valence-ambiguous state** (e.g., wide eyes, open mouth — could be excitement or fear): report both as competing hypotheses with weights, and flag that immediate scene context (not deeper situational inference) is what would resolve it.
