---
name: "facial-expression-affect"
description: "Analyze viewer affect from a clear human face when a transient expression, not identity or situation meaning, is the primary signal. Infer expression direction and activation from multiple visible facial regions, then check body/context congruence and ambiguity. Do not infer personality, trustworthiness, intent, diagnosis, or emotion from a neutral face."
---

# Facial Expression Affect

## Applicability Gate

REQUIRED:
- A human face is large and clear enough to inspect the brow/eye and mouth/jaw regions reliably.
- A transient facial configuration is the dominant affective signal; removing the face would substantially weaken the image's affect.
- At least two independent diagnostic regions support one direction, normally including mouth/jaw plus eye/brow evidence; external hand pressure is not an expression region.

REJECT:
- The face is neutral/resting, too small, blurred, stylized, ambiguous, or lacks a reliable mouth/jaw region; a hand/object distorting or hiding the face lowers applicability rather than proving tension.
- Body posture, infantile morphology, contamination, injury, an unfolding interaction, or visible consequences determine affect more than the face.
- The analysis would infer personality, trustworthiness, dominance, intent, consent, mental illness, pain cause, or moral character.

NEAR MISS:
- Clear whole-body action with an unreadable face -> emotional-body-language.
- Visible event, interaction, stakes, or consequence overrides expression -> cognitive-appraisal.
- Neutral or mildly posed portrait -> no_specialized_skill; explicit social-impression research may use the optional non-VA Todorov module.

ROUTING PRIORITY:
- Prefer this skill only for clear expressive human faces. The presence of a face, direct gaze, attractiveness, identity, or portrait framing alone is insufficient.

## Visual Variables

- **Face reliability**: size, resolution, lighting, angle, occlusion, blur, and visibility of independent facial regions.
- **Brow/forehead configuration**: raised, lowered, drawn together, relaxed, or asymmetric; describe shape without assigning emotion.
- **Eyes/eyelids**: openness, narrowing, lid tension, eye-region contraction, and visible tears; gaze direction is not an emotion.
- **Cheeks/nose region**: cheek raising, nose wrinkling, and mid-face tension when genuinely visible.
- **Mouth/jaw configuration**: corner direction, lip press/stretch, teeth exposure, mouth opening, jaw drop, or relaxed closure.
- **Expression intensity/coherence**: number of converging regions, muscular tension, symmetry, and agreement versus mixed signals.
- **Viewer-transfer modifier**: body, event, interaction, and setting evidence that amplifies or attenuates how strongly the depicted expression should affect a typical viewer.

## Inference Procedure

1. Verify face reliability, independent region visibility, and the removal test; reject neutral faces or configurations without reliable mouth/jaw evidence.
2. Record brow/forehead, eyes/eyelids, cheeks/nose, and mouth/jaw observations without emotion or personality labels.
3. Infer one primary and one plausible alternative affective interpretation from converging regions; mark mixed or posed configurations as uncertain.
4. Estimate depicted expression direction and activation, then assess viewer transfer from visible body/event/context; missing context increases uncertainty and never confirms the expression's cause or intensity.
5. Apply the evidence gate and judge viewer VA conservatively. Treat expression as one-step-removed evidence: do not copy the depicted person's apparent intensity directly into viewer valence or arousal.

## VA Judgment

Use the shared 1-9 scale without fixed emotion-to-VA ranges. A coherent expression provides directional evidence, not a direct transfer of the depicted person's state. Without a visible interaction, consequence, or congruent body signal, keep viewer valence and arousal closer to moderate even when the isolated face appears intense. Arousal requires convergence across regions plus viewer-relevant amplification; direct gaze, teeth, open mouth, eye narrowing, or a single tense region alone is insufficient. Missing context and possible posing increase uncertainty. Reserve extreme viewer scores for expressions embedded in an equally intense, consequential scene.

## Worked Example

- **Image**: A well-lit close face shows symmetric upward mouth corners, raised cheeks, visible eye-region contraction, and a relaxed jaw; the body and background add no conflicting event.
- **Analysis**: reliable face visibility and three converging regions support a positive expression with moderate intensity; no event evidence justifies extreme activation or a claim about personality.
- **VA**: valence 6.4, arousal 4.8 on 1-9; strong expression applicability but conservative viewer impact because the face is isolated and posing remains possible.

## Output Contract

In the shared JSON, report face reliability, mouth/jaw plus eye/brow evidence, expression coherence/intensity, one alternative, viewer-transfer modifiers, and the attenuation from depicted expression to viewer VA. Never infer identity, character, intent, diagnosis, or private emotion as fact.
