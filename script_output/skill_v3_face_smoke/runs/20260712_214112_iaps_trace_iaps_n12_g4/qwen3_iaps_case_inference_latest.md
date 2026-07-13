# qwen3_iaps_case_inference

- time: 2026-07-12T21:42:39
- model_path: /home/u1120250383/dyp/models/qwen
- images: 12
- max_new_tokens: 2048
- full_skill_analysis: False

## 2000.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2000.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.98
- DirectVA: Vscore=8.000; Ascore=6.000; normV=0.875; normA=0.625
- SkillVA: Vscore=8.000; Ascore=5.000; normV=0.875; normA=0.500

### Final skill selection

- selected_skill_id: `facial-expression-affect`
- confidence: 0.0
- fallback: True
- reason: Only one candidate skill analysis succeeded; using it as the final score.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=8.000; Ascore=5.000; normV=0.875; normA=0.500
- seconds: 15.598

**Summary:**
A clear, smiling face with converging positive cues suggests high valence and moderate arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: Wide, open-mouthed smile with visible teeth and raised cheeks; level: high
- variable: brow_eye_visible; observation: Relaxed, slightly upturned eyes with no tension or narrowing; level: high
- variable: face_clear; observation: High-resolution close-up with no blur or occlusion; level: high

**Evidence:**
Wide, toothy smile with raised cheeks and relaxed eyes

**Construct estimates:**
- construct: valence; level: high; basis: Converging positive cues: wide smile, raised cheeks, relaxed eyes
- construct: arousal; level: medium; basis: Positive expression without signs of high activation (e.g., wide eyes, tense jaw) or context amplification

**Uncertainty:**
No body or event context to amplify or attenuate viewer transfer.

**Inference summary:**
Reliable face with converging positive expression cues (mouth, eyes) supports high valence. No signs of high arousal or context amplification, so arousal remains moderate.

### Direct inference

`seconds=28.583`, `input_tokens=1390`, `generated_tokens=140`, `hit_limit=False`

**Summary:**
The subject displays a broad, genuine smile with bright eyes, conveying strong positive affect and moderate to high energy.

**Evidence:**
- wide, toothy smile
- crinkled eyes indicating genuine joy
- vibrant red background enhancing emotional intensity

**Matched emotions:**
- joy
- enthusiasm
- warmth

**Uncertainty:**
Low; facial cues are clear and consistent with high valence and moderate-high arousal.

### Routing inference

`seconds=3.777`, `input_tokens=3969`, `generated_tokens=70`, `hit_limit=False`

**Final decision:**
Clear, smiling human face with visible mouth/jaw and eye/brow regions supporting positive expression.

**Observed cues:**
- smiling mouth
- eye contact
- clear facial features

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=15.598`, `input_tokens=2791`, `generated_tokens=397`, `hit_limit=False`

**Summary:**
A clear, smiling face with converging positive cues suggests high valence and moderate arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: Wide, open-mouthed smile with visible teeth and raised cheeks; level: high
- variable: brow_eye_visible; observation: Relaxed, slightly upturned eyes with no tension or narrowing; level: high
- variable: face_clear; observation: High-resolution close-up with no blur or occlusion; level: high

**Evidence:**
Wide, toothy smile with raised cheeks and relaxed eyes

**Construct estimates:**
- construct: valence; level: high; basis: Converging positive cues: wide smile, raised cheeks, relaxed eyes
- construct: arousal; level: medium; basis: Positive expression without signs of high activation (e.g., wide eyes, tense jaw) or context amplification

**Uncertainty:**
No body or event context to amplify or attenuate viewer transfer.

**Inference summary:**
Reliable face with converging positive expression cues (mouth, eyes) supports high valence. No signs of high arousal or context amplification, so arousal remains moderate.

## 2010.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2010.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.95
- DirectVA: Vscore=7.000; Ascore=5.000; normV=0.750; normA=0.500
- SkillVA: Vscore=7.000; Ascore=5.000; normV=0.750; normA=0.500

### Final skill selection

- selected_skill_id: `direct-va-baseline`
- confidence: 1.0
- fallback: True
- reason: All specialized candidates failed their evidence gate; retaining Direct VA.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=7.500; Ascore=5.500; normV=0.812; normA=0.562
- seconds: 16.796

**Summary:**
A clear, smiling face with visible positive expression cues suggests moderate positive valence and moderate arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: mouth corners are upturned, teeth are visible in a smile, jaw is relaxed; level: high
- variable: brow_eye_visible; observation: eyebrows are relaxed, eyes are open and engaged, no tension; level: high
- variable: cheeks_nose_visible; observation: cheeks are raised, indicating a genuine smile; level: high

**Evidence:**
The mouth and eye regions converge on a positive, relaxed expression with no signs of high activation.

**Construct estimates:**
- construct: valence; level: high; basis: upturned mouth corners, visible teeth, raised cheeks, relaxed eyes indicate a clear positive expression
- construct: arousal; level: medium; basis: expression is positive but not intense; no signs of high activation like wide eyes or tense jaw

**Uncertainty:**
No body or event context is visible to amplify or attenuate the expression's impact.

**Inference summary:**
Reliable face with converging positive cues (mouth, eyes, cheeks) indicates high valence. Absence of high-activation markers (e.g., wide eyes, tense jaw) suggests moderate arousal. No context modifiers apply.

### Direct inference

`seconds=28.641`, `input_tokens=1390`, `generated_tokens=136`, `hit_limit=False`

**Summary:**
The subject's warm smile and direct gaze convey positive affect, while the calm, softly lit setting suggests moderate activation without intensity.

**Evidence:**
- smiling mouth with visible teeth
- direct eye contact
- soft lighting and blurred background

**Matched emotions:**
- contentment
- approachability

**Uncertainty:**
Ambiguity in arousal due to lack of dynamic motion cues; valence is confidently positive from facial expression.

### Routing inference

`seconds=3.551`, `input_tokens=3969`, `generated_tokens=64`, `hit_limit=False`

**Final decision:**
Clear smiling face with visible mouth and eye regions conveying positive affect.

**Observed cues:**
- smiling mouth
- eye contact
- facial expression

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=16.796`, `input_tokens=2785`, `generated_tokens=430`, `hit_limit=False`

**Summary:**
A clear, smiling face with visible positive expression cues suggests moderate positive valence and moderate arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: mouth corners are upturned, teeth are visible in a smile, jaw is relaxed; level: high
- variable: brow_eye_visible; observation: eyebrows are relaxed, eyes are open and engaged, no tension; level: high
- variable: cheeks_nose_visible; observation: cheeks are raised, indicating a genuine smile; level: high

**Evidence:**
The mouth and eye regions converge on a positive, relaxed expression with no signs of high activation.

**Construct estimates:**
- construct: valence; level: high; basis: upturned mouth corners, visible teeth, raised cheeks, relaxed eyes indicate a clear positive expression
- construct: arousal; level: medium; basis: expression is positive but not intense; no signs of high activation like wide eyes or tense jaw

**Uncertainty:**
No body or event context is visible to amplify or attenuate the expression's impact.

**Inference summary:**
Reliable face with converging positive cues (mouth, eyes, cheeks) indicates high valence. Absence of high-activation markers (e.g., wide eyes, tense jaw) suggests moderate arousal. No context modifiers apply.

## 2020.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2020.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.98
- DirectVA: Vscore=8.000; Ascore=6.000; normV=0.875; normA=0.625
- SkillVA: Vscore=8.000; Ascore=6.000; normV=0.875; normA=0.625

### Final skill selection

- selected_skill_id: `facial-expression-affect`
- confidence: 0.0
- fallback: True
- reason: Only one candidate skill analysis succeeded; using it as the final score.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=8.000; Ascore=6.000; normV=0.875; normA=0.625
- seconds: 15.088

**Summary:**
A clear, expressive smile with converging positive cues indicates high valence and moderate-high arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: Wide smile with visible teeth and raised cheeks; level: high
- variable: brow_eye_visible; observation: Eyes crinkled at the corners, indicating genuine smile; level: high
- variable: face_clear; observation: High-resolution close-up with no occlusion or blur; level: high

**Evidence:**
Converging positive cues in mouth, cheeks, and eyes

**Construct estimates:**
- construct: valence; level: high; basis: Wide mouth, raised cheeks, and crinkled eyes converge on positive affect
- construct: arousal; level: medium-high; basis: Smile intensity and eye contraction suggest moderate activation without extreme tension

**Uncertainty:**
No body context to amplify or attenuate viewer transfer

**Inference summary:**
Reliable face with converging positive regions (mouth, eyes) supports high valence. Expression intensity suggests moderate-high arousal, not extreme, due to lack of body context.

### Direct inference

`seconds=28.56`, `input_tokens=1390`, `generated_tokens=137`, `hit_limit=False`

**Summary:**
The subject displays a broad, genuine smile with visible teeth and crinkled eyes, indicating strong positive affect and energetic engagement.

**Evidence:**
- broad smile showing teeth
- crinkled eyes
- raised cheeks
- direct gaze

**Matched emotions:**
- joy
- enthusiasm
- warmth

**Uncertainty:**
No contextual cues suggest deception or forced expression; confidence in positive valence is high.

### Routing inference

`seconds=3.737`, `input_tokens=3969`, `generated_tokens=69`, `hit_limit=False`

**Final decision:**
Clear, expressive smile with visible mouth/jaw and eye/brow regions supporting positive affect.

**Observed cues:**
- wide smile
- eye crinkles
- visible teeth

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=15.088`, `input_tokens=2790`, `generated_tokens=385`, `hit_limit=False`

**Summary:**
A clear, expressive smile with converging positive cues indicates high valence and moderate-high arousal.

**Applicability:**
strong

**Visual evidence:**
- variable: mouth_jaw_visible; observation: Wide smile with visible teeth and raised cheeks; level: high
- variable: brow_eye_visible; observation: Eyes crinkled at the corners, indicating genuine smile; level: high
- variable: face_clear; observation: High-resolution close-up with no occlusion or blur; level: high

**Evidence:**
Converging positive cues in mouth, cheeks, and eyes

**Construct estimates:**
- construct: valence; level: high; basis: Wide mouth, raised cheeks, and crinkled eyes converge on positive affect
- construct: arousal; level: medium-high; basis: Smile intensity and eye contraction suggest moderate activation without extreme tension

**Uncertainty:**
No body context to amplify or attenuate viewer transfer

**Inference summary:**
Reliable face with converging positive regions (mouth, eyes) supports high valence. Expression intensity suggests moderate-high arousal, not extreme, due to lack of body context.

## 2100.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2100.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.98
- DirectVA: Vscore=3.000; Ascore=7.000; normV=0.250; normA=0.750
- SkillVA: Vscore=3.000; Ascore=7.000; normV=0.250; normA=0.750

### Final skill selection

- selected_skill_id: `direct-va-baseline`
- confidence: 1.0
- fallback: True
- reason: All specialized candidates failed their evidence gate; retaining Direct VA.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=3.000; Ascore=8.000; normV=0.250; normA=0.875
- seconds: 20.119

**Summary:**
The face displays a tense, negative expression with high activation, consistent with fear or aggression, supported by converging brow, eye, and mouth cues.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows are lowered and drawn together, indicating tension; level: high
- variable: eyes/eyelids; observation: eyes are wide open with visible tension around the eyelids; level: high
- variable: mouth/jaw; observation: teeth are bared in a grimace or snarl, jaw is tensed; level: high

**Evidence:**
- brows lowered and drawn together
- eyes wide open with tension
- teeth bared and jaw tensed

**Construct estimates:**
- construct: valence; level: low; basis: brow tension, wide eyes, and bared teeth indicate negative affect
- construct: arousal; level: high; basis: converging evidence from brow, eyes, and mouth shows high muscular activation

**Uncertainty:**
No body or event context is visible to confirm or amplify the expression's cause or intensity.

**Inference summary:**
Reliable face with converging negative cues (brow, eye, mouth) indicates low valence. High muscular activation across multiple regions indicates high arousal. Viewer transfer is medium due to lack of context, but expression is strong enough to justify high arousal.

### Direct inference

`seconds=29.218`, `input_tokens=1390`, `generated_tokens=150`, `hit_limit=False`

**Summary:**
The subject displays an intense, confrontational expression with furrowed brows and bared teeth, suggesting anger or aggression, which is high-arousal and negative in valence.

**Evidence:**
- furrowed brow
- bared teeth
- intense eye contact
- tense facial muscles

**Matched emotions:**
- anger
- fear
- aggression

**Uncertainty:**
Ambiguous whether the expression is primarily anger or fear, but both are negative and high-arousal.

### Routing inference

`seconds=3.647`, `input_tokens=3969`, `generated_tokens=69`, `hit_limit=False`

**Final decision:**
Clear human face with tense brow, wide eyes, and bared teeth indicating strong emotion.

**Observed cues:**
- tense brow
- wide eyes
- bared teeth

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=20.119`, `input_tokens=2790`, `generated_tokens=519`, `hit_limit=False`

**Summary:**
The face displays a tense, negative expression with high activation, consistent with fear or aggression, supported by converging brow, eye, and mouth cues.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows are lowered and drawn together, indicating tension; level: high
- variable: eyes/eyelids; observation: eyes are wide open with visible tension around the eyelids; level: high
- variable: mouth/jaw; observation: teeth are bared in a grimace or snarl, jaw is tensed; level: high

**Evidence:**
- brows lowered and drawn together
- eyes wide open with tension
- teeth bared and jaw tensed

**Construct estimates:**
- construct: valence; level: low; basis: brow tension, wide eyes, and bared teeth indicate negative affect
- construct: arousal; level: high; basis: converging evidence from brow, eyes, and mouth shows high muscular activation

**Uncertainty:**
No body or event context is visible to confirm or amplify the expression's cause or intensity.

**Inference summary:**
Reliable face with converging negative cues (brow, eye, mouth) indicates low valence. High muscular activation across multiple regions indicates high arousal. Viewer transfer is medium due to lack of context, but expression is strong enough to justify high arousal.

## 2120.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2120.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.98
- DirectVA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875
- SkillVA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875

### Final skill selection

- selected_skill_id: `facial-expression-affect`
- confidence: 0.0
- fallback: True
- reason: Only one candidate skill analysis succeeded; using it as the final score.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875
- seconds: 16.737

**Summary:**
Intense, negative expression with high activation.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows drawn together and furrowed; level: high
- variable: eyes/eyelids; observation: eyes wide open with intense gaze; level: high
- variable: mouth/jaw; observation: teeth bared in a snarl with lips pulled back; level: high
- variable: expression_intensity; observation: multiple facial regions converge on a tense, aggressive configuration; level: high

**Evidence:**
Converging cues from brow, eyes, and mouth all point to negative valence and high arousal.

**Construct estimates:**
- construct: valence; level: low; basis: brow furrowing, wide eyes, and bared teeth indicate negative affect
- construct: arousal; level: high; basis: intense eye contraction, bared teeth, and tense facial muscles indicate high activation

**Uncertainty:**
No body or event context to override or attenuate the expression.

**Inference summary:**
Reliable face with clear brow, eye, and mouth regions. All regions converge on a negative, high-arousal expression. Viewer transfer is high due to direct gaze and intensity. VA scores reflect the expression's direction and activation.

### Direct inference

`seconds=5.73`, `input_tokens=1390`, `generated_tokens=143`, `hit_limit=False`

**Summary:**
The image depicts a highly intense, angry expression with wide eyes and bared teeth, indicating strong negative emotion and high activation.

**Evidence:**
- furrowed brow
- wide eyes
- bared teeth
- tense facial muscles
- dark background emphasizing intensity

**Matched emotions:**
- anger
- fear
- aggression

**Uncertainty:**
Uncertain if the expression is primarily anger or fear, but both are high-arousal negative states.

### Routing inference

`seconds=3.885`, `input_tokens=3969`, `generated_tokens=76`, `hit_limit=False`

**Final decision:**
Clear human face with intense eye and mouth expression; visible brow, eye, and jaw cues support strong affect.

**Observed cues:**
- intense eye gaze
- brow furrow
- bared teeth

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=16.737`, `input_tokens=2794`, `generated_tokens=426`, `hit_limit=False`

**Summary:**
Intense, negative expression with high activation.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows drawn together and furrowed; level: high
- variable: eyes/eyelids; observation: eyes wide open with intense gaze; level: high
- variable: mouth/jaw; observation: teeth bared in a snarl with lips pulled back; level: high
- variable: expression_intensity; observation: multiple facial regions converge on a tense, aggressive configuration; level: high

**Evidence:**
Converging cues from brow, eyes, and mouth all point to negative valence and high arousal.

**Construct estimates:**
- construct: valence; level: low; basis: brow furrowing, wide eyes, and bared teeth indicate negative affect
- construct: arousal; level: high; basis: intense eye contraction, bared teeth, and tense facial muscles indicate high activation

**Uncertainty:**
No body or event context to override or attenuate the expression.

**Inference summary:**
Reliable face with clear brow, eye, and mouth regions. All regions converge on a negative, high-arousal expression. Viewer transfer is high due to direct gaze and intensity. VA scores reflect the expression's direction and activation.

## 2130.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2130.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.98
- DirectVA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875
- SkillVA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875

### Final skill selection

- selected_skill_id: `facial-expression-affect`
- confidence: 0.0
- fallback: True
- reason: Only one candidate skill analysis succeeded; using it as the final score.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=2.000; Ascore=8.000; normV=0.125; normA=0.875
- seconds: 17.03

**Summary:**
The face displays a clear, intense angry expression with high activation, supported by multiple converging facial regions and no external distortion.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows are furrowed and drawn together; level: high
- variable: eyes/eyelids; observation: eyes are narrowed with visible tension; level: high
- variable: mouth/jaw; observation: mouth is open with teeth bared and jaw tensed; level: high
- variable: expression_intensity; observation: multiple facial regions converge on anger with high muscular tension; level: high

**Evidence:**
bared teeth, furrowed brow, narrowed eyes, tense jaw

**Construct estimates:**
- construct: valence; level: low; basis: furrowed brow, narrowed eyes, bared teeth indicate negative affect
- construct: arousal; level: high; basis: open mouth, bared teeth, tense jaw and brow indicate high activation

**Uncertainty:**
None; expression is unambiguous and fully visible.

**Inference summary:**
Visible evidence of furrowed brow, narrowed eyes, and bared teeth converges on a negative valence. High muscular tension and open mouth indicate high arousal. No context or distortion reduces reliability. Viewer transfer is high due to the direct, unambiguous expression.

### Direct inference

`seconds=5.216`, `input_tokens=1390`, `generated_tokens=132`, `hit_limit=False`

**Summary:**
The subject displays an intense, angry expression with bared teeth and furrowed brows, indicating strong negative emotion and high activation.

**Evidence:**
- bared teeth
- furrowed brows
- tense facial muscles
- open mouth
- intense gaze

**Matched emotions:**
- anger
- fury
- rage

**Uncertainty:**
No contextual cues to suggest underlying motivation or external triggers.

### Routing inference

`seconds=3.59`, `input_tokens=3969`, `generated_tokens=67`, `hit_limit=False`

**Final decision:**
Clear angry facial expression with furrowed brow and bared teeth.

**Observed cues:**
- furrowed brow
- bared teeth
- tense jaw

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=17.03`, `input_tokens=2786`, `generated_tokens=436`, `hit_limit=False`

**Summary:**
The face displays a clear, intense angry expression with high activation, supported by multiple converging facial regions and no external distortion.

**Applicability:**
strong

**Visual evidence:**
- variable: brow/forehead; observation: brows are furrowed and drawn together; level: high
- variable: eyes/eyelids; observation: eyes are narrowed with visible tension; level: high
- variable: mouth/jaw; observation: mouth is open with teeth bared and jaw tensed; level: high
- variable: expression_intensity; observation: multiple facial regions converge on anger with high muscular tension; level: high

**Evidence:**
bared teeth, furrowed brow, narrowed eyes, tense jaw

**Construct estimates:**
- construct: valence; level: low; basis: furrowed brow, narrowed eyes, bared teeth indicate negative affect
- construct: arousal; level: high; basis: open mouth, bared teeth, tense jaw and brow indicate high activation

**Uncertainty:**
None; expression is unambiguous and fully visible.

**Inference summary:**
Visible evidence of furrowed brow, narrowed eyes, and bared teeth converges on a negative valence. High muscular tension and open mouth indicate high arousal. No context or distortion reduces reliability. Viewer transfer is high due to the direct, unambiguous expression.

## 2220.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2220.jpg`
- ok: True
- selected_skill: `facial-expression-affect`
- route_confidence: 0.95
- DirectVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500
- SkillVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500

### Final skill selection

- selected_skill_id: `direct-va-baseline`
- confidence: 1.0
- fallback: True
- reason: All specialized candidates failed their evidence gate; retaining Direct VA.

### Candidate skill analyses

#### 1. facial-expression-affect

- ok: True
- VA: Vscore=4.000; Ascore=6.000; normV=0.375; normA=0.625
- seconds: 17.685

**Summary:**
Intense eye contact and furrowed brow suggest negative valence with moderate-high arousal, but lack of mouth/jaw visibility and hand distortion reduce confidence.

**Applicability:**
partial

**Visual evidence:**
- variable: brow_eye_visible; observation: brows are furrowed and eyes are narrowed with visible tension; level: high
- variable: external_distortion; observation: a finger presses against the nose, deforming the mid-face region; level: high
- variable: mouth_jaw_visible; observation: mouth and jaw are obscured by hand and angle; level: low
- variable: face_clear; observation: face is clear and close-up, but expression is partially occluded; level: medium

**Evidence:**
- furrowed brow and narrowed eyes

**Construct estimates:**
- construct: valence; level: low; basis: furrowed brow and narrowed eyes suggest negative affect, but lack of mouth region prevents confirmation
- construct: arousal; level: medium; basis: intense eye tension and brow furrowing indicate moderate-high activation despite occlusion

**Context modifiers:**
- hand pressing nose obscures mouth/jaw region

**Uncertainty:**
Viewer transfer is low due to lack of body context and possible posing; hand distortion reduces expression reliability.

**Inference summary:**
Furrowed brow and narrowed eyes indicate negative valence and moderate-high arousal, but obscured mouth/jaw and hand distortion limit confidence. Viewer VA is conservative due to partial expression and no contextual amplification.

### Direct inference

`seconds=5.481`, `input_tokens=1390`, `generated_tokens=137`, `hit_limit=False`

**Summary:**
The image shows a close-up of a person's face with intense eye contact and a finger near the nose, conveying a neutral to slightly tense emotional state without clear positive or negative valence.

**Evidence:**
- intense gaze
- finger near nose
- neutral facial expression

**Matched emotions:**
- neutral
- tense
- focused

**Uncertainty:**
Ambiguous emotional intent; could be contemplative, confrontational, or neutral.

### Routing inference

`seconds=3.748`, `input_tokens=3969`, `generated_tokens=72`, `hit_limit=False`

**Final decision:**
Intense eye contact, furrowed brow, and finger near nose suggest strong emotional expression.

**Observed cues:**
- intense gaze
- furrowed brow
- finger near nose

**Candidate skills:**
- facial-expression-affect

### Skill inference

`seconds=17.685`, `input_tokens=2791`, `generated_tokens=455`, `hit_limit=False`

**Summary:**
Intense eye contact and furrowed brow suggest negative valence with moderate-high arousal, but lack of mouth/jaw visibility and hand distortion reduce confidence.

**Applicability:**
partial

**Visual evidence:**
- variable: brow_eye_visible; observation: brows are furrowed and eyes are narrowed with visible tension; level: high
- variable: external_distortion; observation: a finger presses against the nose, deforming the mid-face region; level: high
- variable: mouth_jaw_visible; observation: mouth and jaw are obscured by hand and angle; level: low
- variable: face_clear; observation: face is clear and close-up, but expression is partially occluded; level: medium

**Evidence:**
- furrowed brow and narrowed eyes

**Construct estimates:**
- construct: valence; level: low; basis: furrowed brow and narrowed eyes suggest negative affect, but lack of mouth region prevents confirmation
- construct: arousal; level: medium; basis: intense eye tension and brow furrowing indicate moderate-high activation despite occlusion

**Context modifiers:**
- hand pressing nose obscures mouth/jaw region

**Uncertainty:**
Viewer transfer is low due to lack of body context and possible posing; hand distortion reduces expression reliability.

**Inference summary:**
Furrowed brow and narrowed eyes indicate negative valence and moderate-high arousal, but obscured mouth/jaw and hand distortion limit confidence. Viewer VA is conservative due to partial expression and no contextual amplification.

## 9000.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/9000.jpg`
- ok: True
- selected_skill: `no_specialized_skill`
- route_confidence: 1.0
- DirectVA: Vscore=3.000; Ascore=4.000; normV=0.250; normA=0.375
- SkillVA: Vscore=3.000; Ascore=4.000; normV=0.250; normA=0.375

### Final skill selection

- selected_skill_id: `no_specialized_skill`
- confidence: 1.0
- fallback: False
- reason: No visible direct affective mechanism; symbolic meaning without perceptual stimulation or event-driven stakes.

### Direct inference

`seconds=6.279`, `input_tokens=1390`, `generated_tokens=162`, `hit_limit=False`

**Summary:**
The image evokes somberness and quiet solemnity, with rows of crosses in a forest suggesting remembrance or loss, which is moderately activating due to the structured, repetitive pattern and dim lighting.

**Evidence:**
- dark silhouettes of crosses and trees
- greenish monochromatic tone
- repeating rows creating visual rhythm
- low contrast and subdued lighting

**Matched emotions:**
- sadness
- contemplation
- awe

**Uncertainty:**
Ambiguity in emotional tone due to potential symbolic interpretation of the setting.

### Routing inference

`seconds=2.951`, `input_tokens=3969`, `generated_tokens=52`, `hit_limit=False`

**Final decision:**
No visible direct affective mechanism; symbolic meaning without perceptual stimulation or event-driven stakes.

## 2597.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/2597.jpg`
- ok: True
- selected_skill: `no_specialized_skill`
- route_confidence: 0.99
- DirectVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500
- SkillVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500

### Final skill selection

- selected_skill_id: `no_specialized_skill`
- confidence: 0.99
- fallback: False
- reason: Routine social gathering with no visible consequential event, threat, or perceptual novelty driving affect.

### Direct inference

`seconds=5.411`, `input_tokens=1390`, `generated_tokens=133`, `hit_limit=False`

**Summary:**
The scene depicts a crowded, busy market with people gathered around a counter, suggesting moderate social energy without overt emotional positivity or negativity.

**Evidence:**
- crowded space with many people
- bright artificial lighting
- presence of food and commerce

**Matched emotions:**
- neutral engagement
- moderate social excitement

**Uncertainty:**
Ambiguous emotional tone due to lack of clear facial expressions or contextual cues indicating joy or stress.

### Routing inference

`seconds=3.382`, `input_tokens=3969`, `generated_tokens=63`, `hit_limit=False`

**Final decision:**
Routine social gathering with no visible consequential event, threat, or perceptual novelty driving affect.

**Observed cues:**
- crowd at counter
- market signage
- ambient lighting

## 7080.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/7080.jpg`
- ok: True
- selected_skill: `no_specialized_skill`
- route_confidence: 1.0
- DirectVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500
- SkillVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500

### Final skill selection

- selected_skill_id: `no_specialized_skill`
- confidence: 1.0
- fallback: False
- reason: Plain object on neutral background; no affective mechanism visible.

### Direct inference

`seconds=5.056`, `input_tokens=1390`, `generated_tokens=128`, `hit_limit=False`

**Summary:**
The image presents a simple, static object on a textured surface, evoking neither strong positive nor negative affect, with moderate visual engagement.

**Evidence:**
- plain fork on uniform background
- neutral color palette
- lack of dynamic elements

**Matched emotions:**
- indifference
- calm observation

**Uncertainty:**
Ambiguous emotional context due to minimal visual cues beyond object placement.

### Routing inference

`seconds=2.743`, `input_tokens=3969`, `generated_tokens=46`, `hit_limit=False`

**Final decision:**
Plain object on neutral background; no affective mechanism visible.

## 5870.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/5870.jpg`
- ok: True
- selected_skill: `no_specialized_skill`
- route_confidence: 1.0
- DirectVA: Vscore=6.000; Ascore=5.000; normV=0.625; normA=0.500
- SkillVA: Vscore=6.000; Ascore=5.000; normV=0.625; normA=0.500

### Final skill selection

- selected_skill_id: `no_specialized_skill`
- confidence: 1.0
- fallback: False
- reason: No specialized affective mechanism is visibly dominant; cloud scene lacks scale cues, threat, novelty, or restorative structure.

### Direct inference

`seconds=6.043`, `input_tokens=1390`, `generated_tokens=152`, `hit_limit=False`

**Summary:**
The image presents a serene yet dynamic sky with voluminous clouds, evoking a calm but engaging visual experience.

**Evidence:**
- soft blue sky with bright white clouds
- clouds show texture and depth without threatening intensity
- no strong emotional cues like storm or desolation

**Matched emotions:**
- serene
- contemplative
- calm

**Uncertainty:**
Ambiguity in arousal due to lack of motion cues; cloud formation suggests potential for change but not immediate threat.

### Routing inference

`seconds=3.21`, `input_tokens=3969`, `generated_tokens=58`, `hit_limit=False`

**Final decision:**
No specialized affective mechanism is visibly dominant; cloud scene lacks scale cues, threat, novelty, or restorative structure.

## 4670.jpg

- image: `/home/u1120250383/dcs/datasets/IAPS/Dataset/4670.jpg`
- ok: True
- selected_skill: `no_specialized_skill`
- route_confidence: 1.0
- DirectVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500
- SkillVA: Vscore=5.000; Ascore=5.000; normV=0.500; normA=0.500

### Final skill selection

- selected_skill_id: `no_specialized_skill`
- confidence: 1.0
- fallback: False
- reason: No specialized affective mechanism visibly dominant; intimate body contact without clear arousal/valence cues or direct appraisal stakes.

### Direct inference

`seconds=7.648`, `input_tokens=1390`, `generated_tokens=197`, `hit_limit=False`

**Summary:**
The image depicts an intimate, physically close moment between two nude individuals, suggesting a context of affection or passion. The visual composition is warm and focused on the bodies, but lacks overtly positive or negative emotional cues, leading to a neutral valence. The physical closeness and implied intimacy suggest moderate activation, not extreme calm or high excitement.

**Evidence:**
- nude bodies in close physical contact
- intimate posture
- warm lighting
- lack of facial expressions to gauge emotion

**Matched emotions:**
- affection
- intimacy
- neutral affect

**Uncertainty:**
Valence is inferred as neutral due to absence of clear emotional indicators; arousal is moderate based on implied intimacy without visual cues of extreme passion or calm.

### Routing inference

`seconds=3.782`, `input_tokens=3969`, `generated_tokens=73`, `hit_limit=False`

**Final decision:**
No specialized affective mechanism visibly dominant; intimate body contact without clear arousal/valence cues or direct appraisal stakes.

**Observed cues:**
- naked human bodies
- intimate embrace
- no visible face or expressive body language
