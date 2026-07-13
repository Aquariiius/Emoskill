# qwen3_iaps_case_inference

- time: 2026-07-12T21:41:12
- model_path: /home/u1120250383/dyp/models/qwen
- images: 3
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
