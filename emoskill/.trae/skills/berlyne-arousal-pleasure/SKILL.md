---
name: "berlyne-arousal-pleasure"
description: "Analyzes images with Berlyne's arousal-aesthetic pleasure model (collative variables, arousal potential, inverted-U hedonic value) and maps aesthetic stimulation into valence-arousal. Use for images where affect is driven by visual/compositional properties — novelty, complexity, ambiguity, incongruity — that demand active engagement (hard fascination), especially artwork, design, and visually striking or unusual scenes. Do NOT use for calm, restful, coherent natural or spatial scenes with effortless (soft) fascination — use Kaplan ART instead. Do NOT use when the emotional charge comes from depicted narrative, social, or situational content rather than the aesthetics of the rendering itself — use Cognitive Appraisal or PANAS. Do NOT use for face-centered structural impressions (Todorov)."
---

# Berlyne Arousal-Aesthetic Pleasure

## Purpose

Use this skill when an image's affect is best explained by the aesthetics of stimulation itself: how novel, complex, ambiguous, or surprising the visual/compositional properties are, and how that arousal potential translates into pleasure or displeasure. Berlyne's model proposes an inverted-U (Wundt curve) relationship between arousal potential and hedonic value: too little stimulation is boring (low arousal, flat/mildly negative valence), a moderate amount is pleasurable (the sweet spot of interest and liking), and too much becomes overwhelming or aversive (high arousal, negative valence). This skill's job is to locate an image on that curve — not to explain narrative or social emotion, and not to describe calm/restful environments (that's soft fascination, Kaplan's territory).

## Core Constructs

- **Collative variables** — novelty, complexity, ambiguity, incongruity, surprise: properties that arise from comparing the stimulus to expectation/prior experience, and that drive arousal potential.
- **Arousal potential** — the overall activation the collative variables (plus psychophysical intensity, e.g. color/contrast/scale) are likely to produce in a viewer.
- **Hedonic value** — the resulting pleasure or displeasure, following an inverted-U: peaking at moderate arousal, dropping off at both very low (boring) and very high (overwhelming) arousal.

## Use When

Invoke this skill when:

- The image's affect depends mainly on aesthetic stimulation — composition, novelty, visual complexity, unusual arrangement — rather than a clear human emotion or narrative.
- The scene is visually rich, unusual, complex, ambiguous, or compositionally striking, and this perceptual quality (not depicted events) is the source of arousal.
- The task concerns aesthetic pleasure, preference, visual interest, or stimulation.
- The image demands active visual engagement (hard fascination) rather than offering effortless rest.

## Do-Not-Use-When Rules

Do not use this skill when:

- The scene is calm, coherent, and restful — low collative arousal, effortless (soft) fascination → defer to **Kaplan ART**.
- The "novelty," "ambiguity," or "surprise" in the image is really about **narrative or social content** (a shocking event, an unexpected social situation) rather than perceptual/compositional properties → defer to **Cognitive Appraisal** or **PANAS**.
- The image contains disturbing or threatening content whose arousal is driven by perceived threat rather than aesthetic stimulation → defer to **Cognitive Appraisal**.
- A face is the dominant subject with a neutral/mild expression → defer to **Todorov**.

## Routing / Self-Check

Before proceeding:

1. **Is the arousal/affect driven by visual-perceptual properties (composition, novelty, complexity) or by situational/narrative content (what's happening, to whom, why)?** If the latter, defer to Appraisal or PANAS.
2. **Is the scene calm and coherent (soft fascination) rather than stimulating (hard fascination)?** If calm/restful, defer to Kaplan — this is the key discriminator between the two aesthetic/environment skills.
3. If the affect is genuinely driven by perceptual stimulation properties and the scene is not simply restful, proceed.

State which check applied in the output.

## Reasoning Steps

1. **Self-check routing** — confirm the driver is aesthetic/perceptual stimulation, not narrative content or restful coherence; if not, name the better-fitting skill.
2. Describe visible composition, order, novelty, and sensory density.
3. Estimate novelty, complexity, ambiguity, and surprise from image evidence (collative variables).
4. Judge where the resulting arousal potential falls: low (understimulating), moderate (engaging), or excessive (overwhelming) — this determines position on the inverted-U.
5. Infer likely aesthetic pleasure or displeasure from that position, not simply from arousal magnitude alone.
6. Convert the aesthetic judgment into final VA, reflecting the inverted-U (moderate arousal → more positive valence; very low or very high arousal → flatter or more negative valence).

## Output Format

```
ROUTING CHECK: [why this is aesthetic-stimulation-driven, not narrative/social or restful]
COLLATIVE VARIABLES: [novelty / complexity / ambiguity / surprise, each with visible evidence]
AROUSAL POTENTIAL: [low / moderate / excessive, with justification]
INVERTED-U POSITION: [where the estimated arousal falls on the Wundt curve, and what that implies for hedonic value]
LIKELY PLEASURE OR DISPLEASURE: [qualitative judgment]
FINAL VALENCE: [value + justification]
FINAL AROUSAL: [value + justification]
UNCERTAINTY NOTES: [ambiguity, individual variation in optimal stimulation level, image quality]
```

## Uncertainty and Ethical Constraints

The inverted-U relationship is a general tendency, not a fixed rule — individuals vary in preferred stimulation level, and empirical support for the exact inverted-U shape is mixed in the literature, so treat position on the curve as a reasoned estimate rather than a precise measurement. Avoid conflating high arousal from disturbing/threatening content with high arousal from aesthetic stimulation — these have different valence implications and different skill homes (the latter stays here; the former belongs to Appraisal). Don't assume a single "correct" hedonic response; note when reasonable viewers might disagree.

## Examples That Should Trigger

- An abstract painting with bold, unusual color relationships and ambiguous forms.
- A striking piece of architecture with an unconventional, complex structure.
- A surreal or dreamlike digital artwork with incongruous elements.

## Examples That Should NOT Trigger

- A calm, coherent forest scene with soft light → Kaplan (soft fascination, restful).
- A chaotic scene of a car accident → Cognitive Appraisal (arousal driven by threat/narrative, not aesthetics).
- A joyous, visually busy birthday party → PANAS (affect driven by depicted emotion, not composition).
- A neutral close-up portrait, however well-lit → Todorov (face-dominant, structural read).

## Ambiguous Cases

- **Visually complex disaster or crime scene:** complexity and surprise are present, but the arousal is threat/narrative-driven, not aesthetic → defer to Cognitive Appraisal, and note this explicitly during the self-check.
- **Dramatic but coherent landscape (e.g., a vivid sunset over mountains):** if the dominant quality is effortless awe/calm, lean Kaplan; if it's more about unusual, striking visual novelty demanding engagement, lean Berlyne. Name the ambiguity and pick based on which quality is more visually dominant.
- **Portrait-as-artwork with striking style:** if the depicted person's expression/structure still drives the read, defer to Todorov/PANAS; if the rendering/style itself (not the sitter) is what's aesthetically striking, proceed with Berlyne.
