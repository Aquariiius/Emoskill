---
name: "facial-expression-affect"
description: "Analyze viewer affect from a clear TRANSIENT human facial expression when the face is dominant and readable. Requires independent brow/eye and mouth/jaw evidence for a coherent expression; neutral, ambiguous, occluded, or hand-distorted faces must gate to use_direct. Do not use for personality impressions, body-carried emotion, or event-driven scenes."
---

# Facial Expression Affect

## Applicability Gate

REQUIRED:
- A human face is the dominant subject and large/clear enough to read.
- Brow/eye region AND mouth/jaw region independently support the SAME transient expression.
- The expression, not an event, object, or body action, carries the affect.

REJECT:
- Neutral, resting, or ambiguous face; structural first impressions are out of scope.
- Hand or object presses, covers, or visibly deforms a diagnostic region (external_distortion).
- A consequential event or interaction determines affect -> cognitive-appraisal; whole-body signal -> emotional-body-language; infant morphology -> baby-schema.

NEAR MISS:
- Smiling person inside a larger meaningful event -> cognitive-appraisal if the event dominates.
- Crying/laughing crowd where no single face is readable -> emotional-body-language.

## Visual Variables

- **Face reliability**: face_clear, brow_eye_visible, mouth_jaw_visible, external_distortion — all as observable booleans.
- **Region evidence**: brow position, eye aperture, mouth curvature/opening, jaw tension; record separately.
- **Coherence/intensity**: do independent regions agree, and how strong is the display (mild, clear, extreme)?
- **Viewer transfer**: does visible body/context support the viewer sharing the affect (amplifiers/attenuators)?

## Inference Procedure

1. Fill face_reliability booleans first; any false diagnostic region or distortion -> gate_decision use_direct.
2. Record brow/eye and mouth/jaw observations without emotion labels.
3. Infer the primary expression and one alternative; require region coherence.
4. Estimate intensity and viewer_transfer (level low/medium/high with amplifiers/attenuators).
5. If gate passes, judge VA with the anchors; otherwise output conservative scores and use_direct.

## Arousal Gate

Expression valence transfers more reliably than intensity: a posed smile is calm content.
Raise arousal above 5 only for high-intensity displays with a visible activation cue (open-mouth
laughter, screaming, wide-eyed fear, rage tension). Mild smiles, quiet sadness, and posed
portraits are NOT activation cues. No activation cue -> arousal <= 4.5.

## VA Anchors (1-9)

| Expression | Valence | Arousal |
|---|---:|---:|
| Clear smile, relaxed happiness | 6.8-7.8 | 4.4-5.4 |
| Open laughter, excitement | 7.2-8.2 | 5.4-6.4 |
| Sadness, quiet crying | 2.6-3.6 | 4.2-5.2 |
| Anger, visible rage tension | 2.8-3.8 | 5.6-6.6 |
| Fear, wide-eyed alarm | 3.0-4.0 | 6.0-7.0 |
| Mild/ambiguous display (gate to use_direct if unsure) | 4.5-6.0 | 4.0-5.0 |

Anchors are typical bands, not forced outputs; interpolate, and with thin evidence stay at the
band edge closest to neutral.

## Worked Examples

- **Activated**: A woman laughs with open mouth, raised cheeks, and crinkled eyes filling the
  frame. -> coherent high-intensity joy, both regions agree; activation_evidence ["open-mouth
  laughter"]. gate_decision use_skill. **V 7.6, A 6.0**, strong.
- **Calm**: A man looks down with drawn brows, downturned mouth, a single tear on his cheek. ->
  coherent quiet sadness, no motion or urgency; activation_evidence []. gate_decision
  use_skill. **V 3.0, A 4.6**, strong.

## Output Contract

The shared JSON MUST include face_reliability (four booleans), viewer_transfer
(level/amplifiers/attenuators), gate_decision (use_skill|use_direct), and top-level
`activation_evidence` (empty list if none). Report perceived expression, never identity,
personality, or the person's true inner state.
