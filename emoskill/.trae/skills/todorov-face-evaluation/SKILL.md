---
name: "todorov-face-evaluation"
description: "Analyzes face-dominant images using Oosterhof & Todorov's two-dimensional social evaluation model (trustworthiness/valence and dominance) to estimate the automatic, low-information first impression a viewer forms from facial structure, then maps that impression into valence-arousal space. Use when a specific human face is the dominant subject AND the face is neutral, resting, or only mildly expressive, so the affective read comes from structural social evaluation (trust, threat, warmth, authority, intimidation, approach/avoidance) rather than a clearly legible discrete emotion. Do NOT use for faces showing an obvious strong expression (crying, laughing, screaming, visible fear/anger/joy) — route those to PANAS or Cognitive Appraisal instead. Do NOT use when the affect depends on situational context rather than facial structure, or when the image is primarily a landscape, artwork, or scene rather than a face."
---

# Todorov Face Evaluation

## Purpose

Model the fast, automatic social first impression a viewer forms from a face's static structure — trustworthiness and dominance — and translate that impression into valence-arousal (VA) coordinates. This captures a face-based effect that is distinct from recognizing an expressed emotion: it is about what a face's *shape* silently signals about the person's likely intent and capability, independent of whether they are currently expressing a feeling.

This model was built on judgments of **emotionally neutral faces**. It explains a real but easily-confused phenomenon: humans read resting facial structure (brow shape, mouth curvature at rest, jaw width, eye shape) through the lens of expression categories, even absent real expression. A face that structurally resembles anger is read as less trustworthy; a face that structurally resembles happiness is read as more trustworthy — even when the person is not currently expressing anger or happiness at all. Dominance is a separate axis, tied to features that read as masculine, mature, or physically capable, signaling ability to cause harm rather than intent to.

## Core Constructs

- **Trustworthiness / valence** — perceived intention to help or harm; approach vs. avoid. Driven by resemblance to emotional expression categories at rest (subtle warmth vs. subtle threat in neutral structure).
- **Dominance** — perceived capability to exert power or inflict harm; driven by cues resembling masculinity, maturity, and physical strength (jaw/brow structure, facial width-to-height ratio).
- **Approach/avoidance tendency** — the behavioral inference that follows from trustworthiness (not from dominance).
- **Youthful-attractiveness (optional, secondary)** — a smaller, later-identified third factor. Note it only if visibly salient; do not treat it as a primary axis.

## Use-When Rules

Use this skill only when **both** conditions hold:

1. A specific human face is the dominant subject of the image (portrait, headshot, close/medium shot where the face is clearly resolvable).
2. The face is neutral, resting, or only mildly/ambiguously expressive — the viewer's affective reaction plausibly comes from facial *structure* (shape of eyes, brows, jaw, mouth at rest) rather than a clearly readable emotional display.

Typical fits: professional headshots, ID-style or passport-style photos, candid portraits with a relaxed or composed expression, official portraits (e.g., leaders, professionals) evaluated for perceived trustworthiness/authority, character-design or casting-style "what impression does this face give" questions.

## Do-Not-Use-When Rules

Do not use this skill when:

- The face shows a **clear, strong discrete emotion** (crying, laughing, screaming, visibly furious, visibly terrified, ecstatic). That is expression recognition, not structural evaluation → defer to **PANAS**.
- The emotional read depends on **understanding the situation** — why the person looks that way, what just happened, who is responsible, what's at stake → defer to **Cognitive Appraisal**.
- The face is present but **incidental** — the image is really about an environment, landscape, or restorative setting with a person in it → defer to **Kaplan ART**.
- The image's affective pull comes from **composition, style, or rendering** rather than the depicted person's face itself (e.g., an abstract or heavily stylized portrait valued for its aesthetics) → defer to **Berlyne**.
- No face is clearly resolvable, or multiple faces are equally weighted with no clear primary subject (see Ambiguous Cases below).

## Routing / Deferral Rules

Run this self-check before proceeding:

1. **Is a face the dominant subject?** If no → stop, defer to the skill matching the actual dominant content (Kaplan for environment, Berlyne for aesthetic/compositional focus).
2. **Is the face's expression neutral-to-mild, or strong-and-legible?** If strong and legible → stop, defer to PANAS (or Appraisal if situational context is doing the interpretive work).
3. **Does resolving the affect require knowing the surrounding situation** (context, causality, social stakes) rather than reading the face alone? If yes → defer to Cognitive Appraisal.
4. If none of the above deferrals apply, proceed with Todorov-style analysis.

State explicitly in the output which check passed and why this skill (rather than another) was judged appropriate.

## Reasoning Steps

1. **Self-check routing** (see above) — confirm this is genuinely a structural/evaluative case, not expression recognition or context-dependent appraisal. If it fails, say so and name the more appropriate skill instead of proceeding.
2. Identify the primary face and describe its salient structural features (brow angle, eye shape/spacing, mouth curvature at rest, jaw/facial width, apparent age/maturity cues) — visible evidence only.
3. Estimate **trustworthiness** from structural resemblance to warmth/threat expression categories, independent of any actual current expression.
4. Estimate **dominance** from structural resemblance to strength/maturity/authority cues.
5. Combine the two into a social-affective impression (e.g., high trust + low dominance → warm/approachable; low trust + high dominance → intimidating/threatening; high trust + high dominance → authoritative-but-safe; low trust + low dominance → weak/untrustworthy).
6. Convert this impression into final valence and arousal, and note confidence.
7. Add the required ethical framing (see below) before finalizing output.

## Output Format

```
ROUTING CHECK: [confirmation this skill applies + which deferral checks were considered and ruled out]
FACIAL EVIDENCE: [visible structural features observed]
TRUSTWORTHINESS ESTIMATE: [low/mid/high + supporting cues]
DOMINANCE ESTIMATE: [low/mid/high + supporting cues]
SOCIAL IMPRESSION: [combined qualitative read, e.g. "warm and non-threatening" / "authoritative and mildly intimidating"]
FINAL VALENCE: [value + brief justification]
FINAL AROUSAL: [value + brief justification]
UNCERTAINTY: [confidence level, ambiguous cues, image quality/pose/occlusion limitations]
ETHICAL NOTE: [one line reframing this as a perceived first impression, not a fact about the person]
```

## Uncertainty and Ethical Constraints

This model describes a fast, automatic, and **often inaccurate** perceptual stereotype — not a valid measure of a person's real character, morality, trustworthiness, or intentions. Face-evaluation research has documented real-world biases from this exact effect (e.g., correlations between perceived facial "competence" and election outcomes, and between perceived facial "trustworthiness" and sentencing disparities for the same crime). Because of this:

- Always frame output as "this face is likely to be *perceived* as..." never as "this person is...".
- Never assert claims about the real person's actual personality, honesty, competence, or moral character.
- Flag when demographic features (age, gender presentation, race, disability-related features) may be driving the trustworthiness/dominance read, since these evaluations are known to correlate with — and reproduce — demographic stereotyping. Do not use this skill to make or imply judgments about identity groups.
- If the face is a public figure, keep the analysis to the *impression a viewer might form*, not a claim about who they really are.
- If image quality, occlusion, non-frontal pose, or stylization (illustration, heavy filter, low resolution) limits reliable structural reading, say so explicitly and widen uncertainty rather than guessing confidently.

## Examples That Should Trigger

- "What kind of first impression does this headshot give?"
- A neutral-expression professional portrait used for a casting or character-design decision.
- "Does this person look trustworthy in this photo?"
- A relaxed, composed passport-style photo being rated for perceived authority/approachability.

## Examples That Should NOT Trigger

- A photo of someone sobbing at a funeral → PANAS or Appraisal (clear discrete emotion + situational meaning).
- "Why does this person look so frustrated in this meeting photo?" → Cognitive Appraisal (context-dependent).
- A hiker's small silhouette against a mountain vista → Kaplan (face incidental, environment dominant).
- A painterly, abstract portrait praised for its brushwork and color → Berlyne (aesthetic/compositional driver).
- A joyfully laughing crowd at a concert → PANAS (strong legible discrete emotion, not structural read).

## Ambiguous Cases

- **Multiple faces, no clear primary subject:** if faces are roughly equal in prominence, either (a) pick the most foregrounded/largest face and analyze it as primary, noting the choice, or (b) if the image is really about group dynamics, defer to Cognitive Appraisal instead.
- **Mild expression, unclear whether "neutral enough":** if uncertain, proceed with Todorov analysis but explicitly flag in UNCERTAINTY that a mild expression may be contributing beyond pure structural read.
- **Stylized/illustrated/painted faces:** proceed cautiously — the model was built on photographic faces — and flag reduced confidence due to non-photographic rendering.
- **Face + strong environment, both salient:** if the face is large/foregrounded and clearly the subject, use Todorov for the face and mention environment only as context; if the environment is equally or more dominant, defer to Kaplan/Berlyne instead.
