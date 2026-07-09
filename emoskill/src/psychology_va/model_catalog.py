from __future__ import annotations

from .schemas import PsychologySkillSpec


def build_default_skill_specs() -> list[PsychologySkillSpec]:
    return [
        PsychologySkillSpec(
            skill_id="kaplan-art-restoration",
            display_name="Kaplan ART Restoration",
            short_description="Estimates restorative affect through attention restoration cues such as being-away, fascination, extent, and compatibility, then projects the result into VA.",
            theory_family="attention-restoration-theory",
            selection_hints=[
                "the image is a landscape, built environment, or everyday setting with restorative potential",
                "the task concerns calmness, mental recovery, attentional relief, or environmental preference",
                "nature, greenery, water, openness, refuge, or coherent spatial layout is visually salient",
            ],
            use_when=(
                "Use when the image should be analyzed through Kaplan's Attention Restoration Theory, "
                "especially for natural scenes, restorative environments, and attention-recovery related affect."
            ),
            image_signals=[
                "being-away cues such as escape from routine or urban pressure",
                "soft fascination such as water, foliage, sky, depth, or patterned natural detail",
                "extent or coherence of the environment",
                "compatibility between scene affordances and likely viewer goals",
                "refuge, openness, safety, and restorative spatial structure",
            ],
            va_focus=(
                "Estimate VA from restorative potential: high restoration usually implies more positive valence "
                "and lower to moderate arousal rather than high-activation excitement."
            ),
            analysis_steps=[
                "identify environmental features relevant to being-away, fascination, extent, and compatibility",
                "estimate overall restorative potential from visible evidence",
                "infer the likely affective consequence of restoration for the viewer",
                "project the restorative state into valence-arousal space",
                "explain uncertainty when scene function or viewer context is unclear",
            ],
        ),
        PsychologySkillSpec(
            skill_id="berlyne-arousal-pleasure",
            display_name="Berlyne Arousal-Pleasure",
            short_description="Estimates VA from collative variables such as novelty, complexity, ambiguity, and surprise within Berlyne's arousal-aesthetic pleasure framework.",
            theory_family="berlyne-arousal-aesthetics",
            selection_hints=[
                "the image is artwork, design, architecture, installation, or a visually rich scene",
                "novelty, complexity, ambiguity, surprise, or pattern density drives the viewing experience",
                "the task concerns aesthetic preference, interest, stimulation, or hedonic response",
            ],
            use_when=(
                "Use when the image should be interpreted through Berlyne's arousal-aesthetic pleasure model, "
                "especially when collative properties drive the final affective response."
            ),
            image_signals=[
                "novelty or unexpected composition",
                "visual complexity or information density",
                "ambiguity and interpretive openness",
                "pattern richness, contrast, and sensory stimulation",
                "order-disorder balance affecting aesthetic pleasure",
            ],
            va_focus=(
                "Estimate how collative variables shape arousal potential and aesthetic pleasure, then convert that judgment into final VA."
            ),
            analysis_steps=[
                "identify novelty, complexity, ambiguity, surprise, and regularity cues",
                "estimate the scene's arousal potential",
                "judge likely aesthetic pleasure or displeasure from the balance of stimulation",
                "project the inferred affective state into valence-arousal space",
                "state whether the scene exceeds or falls below an optimal stimulation range",
            ],
        ),
        PsychologySkillSpec(
            skill_id="todorov-face-evaluation",
            display_name="Todorov Face Evaluation",
            short_description="Analyzes faces with Todorov's two-dimensional social evaluation model using trustworthiness and dominance cues, then maps the inferred social impression into VA.",
            theory_family="todorov-face-evaluation",
            selection_hints=[
                "a human face is the main visual target",
                "the task depends on first impressions such as trustworthiness, warmth, threat, dominance, or competence-like face impression",
                "facial morphology and expression cues matter more than landscape restoration or aesthetic collative variables",
            ],
            use_when=(
                "Use when image VA analysis should be grounded in Todorov's face evaluation framework, "
                "especially for portraits, close-up faces, and socially evaluative face impressions."
            ),
            image_signals=[
                "facial trustworthiness cues such as warmth, friendliness, or threat reduction",
                "facial dominance cues such as strength, authority, or intimidation",
                "eye region tension and brow configuration",
                "mouth curvature and expressive softness or hardness",
                "face angle, symmetry, and salient first-impression cues",
            ],
            va_focus=(
                "Infer trustworthiness and dominance from facial cues, then estimate final valence and arousal from the resulting social-evaluative impression."
            ),
            analysis_steps=[
                "identify the primary face and relevant portrait cues",
                "estimate trustworthiness-related impression from visible facial evidence",
                "estimate dominance-related impression from visible facial evidence",
                "combine the two dimensions into an overall social-affective impression",
                "project the resulting impression into valence-arousal space and explain uncertainty",
            ],
        ),
        PsychologySkillSpec(
            skill_id="evolved-fear-module",
            display_name="Evolved Fear Module",
            short_description=(
                "Analyzes images containing evolutionarily threatening animals (snakes, spiders, large predators) "
                "using Öhman & Mineka's evolved fear module — an automatic, cognitively encapsulated threat-detection "
                "system — and maps the fear response into VA."
            ),
            theory_family="evolved-fear-module",
            selection_hints=[
                "a snake, spider, scorpion, or large predator is the dominant visual content",
                "the animal displays ancestral threat morphology: serpentine coils, arachnid legs, bared fangs, predatory crouch",
                "the viewer's likely response is automatic fear rather than disgust or general threat appraisal",
            ],
            use_when=(
                "Use when the image's dominant affective content is a fear-relevant animal whose body form "
                "matches ancestral threat morphology. Do not use for general danger without a specific threat animal."
            ),
            image_signals=[
                "serpentine body coils or S-shaped form",
                "arachnid leg configuration or spider-like body",
                "bared fangs, venom apparatus, or claws",
                "predatory crouch, stalking posture, or strike-ready stance",
                "concealment in vegetation or ambush positioning",
            ],
            va_focus=(
                "Estimate fear intensity from threat imminence (proximity, posture, visibility) modulated by "
                "context attenuation (cartoon, toy, glass enclosure, distance). Higher threat → more negative V, higher A."
            ),
            analysis_steps=[
                "confirm a fear-relevant animal is the dominant content, not disgust or general threat",
                "identify the animal species/type and visible threat morphology",
                "assess threat imminence from posture, proximity, concealment, and orientation",
                "assess context attenuation from safety cues (glass, cartoon, toy, distance, pet context)",
                "estimate VA from threat imminence modulated by attenuation",
            ],
        ),
        PsychologySkillSpec(
            skill_id="pathogen-disgust",
            display_name="Pathogen Disgust",
            short_description=(
                "Analyzes images containing contamination, decay, bodily waste, wounds, or pest infestation "
                "using Tybur et al.'s three-domain disgust framework (pathogen domain) and the behavioral "
                "immune system, then maps the disgust response into VA."
            ),
            theory_family="pathogen-disgust",
            selection_hints=[
                "the image shows rot, mold, bodily fluids, pus, open wounds, insect infestation, feces, or decay",
                "the viewer's likely response is revulsion and withdrawal rather than fear and flight",
                "contamination or disease-signaling cues dominate the scene rather than predatory threat",
            ],
            use_when=(
                "Use when the image's dominant affective content involves visible contamination, decay, or "
                "disease cues. Do not use for predatory animals (Fear Module) or moral violations (Cognitive Appraisal)."
            ),
            image_signals=[
                "organic decay, rot, or decomposition",
                "bodily fluids: blood pooling, vomit, pus, feces",
                "mold, mildew, or fungal growth on surfaces",
                "insect or pest infestation associated with disease",
                "spoiled food with discoloration or slime",
            ],
            va_focus=(
                "Estimate disgust intensity from contamination severity, modulated by context exemptions "
                "(medical, culinary, fictional). Disgust arousal is characteristically lower than fear arousal."
            ),
            analysis_steps=[
                "confirm contamination/pathogen cues dominate, not predatory threat or moral violation",
                "identify and describe contamination cues: type, extent, and intensity",
                "assess contamination intensity: mild, moderate, or severe",
                "check for context exemptions: medical, culinary, fictional, academic",
                "estimate VA with disgust-appropriate arousal (lower than fear for comparable severity)",
            ],
        ),
        PsychologySkillSpec(
            skill_id="baby-schema",
            display_name="Baby Schema / Kindchenschema",
            short_description=(
                "Analyzes images containing infantile or cute subjects using Lorenz's Kindchenschema and "
                "Glocker et al.'s findings — neotenic features (large head, round face, big eyes) trigger "
                "cuteness perception and caregiving motivation — then maps into VA."
            ),
            theory_family="baby-schema",
            selection_hints=[
                "the dominant subject is an infant, baby animal, or character with neotenic design",
                "the viewer's likely response is cuteness, tenderness, or caregiving motivation",
                "infantile body proportions (large head ratio, round face, big eyes) drive the affective read",
            ],
            use_when=(
                "Use when the image's dominant subject displays baby schema features: human infants, animal "
                "babies, or deliberately neotenic characters/products. Do not use for adult faces (Todorov)."
            ),
            image_signals=[
                "large head-to-body ratio",
                "high protruding forehead and round face shape",
                "large eyes positioned low on the face",
                "chubby cheeks, small nose, and small mouth",
                "short stubby limbs and round plump body",
            ],
            va_focus=(
                "Estimate cuteness response from baby schema feature load. High load + safe context → "
                "positive V, low-moderate A (warm, tender approach). Distress or uncanny context overrides."
            ),
            analysis_steps=[
                "confirm baby schema features are dominant and context is safe/benign",
                "identify visible baby schema features from the morphological checklist",
                "estimate baby schema load: low, moderate, or high",
                "check for affect-overriding context: distress, illness, exploitation, uncanny wrongness",
                "estimate VA from schema load and context, typically V positive, A low-moderate",
            ],
        ),
        PsychologySkillSpec(
            skill_id="emotional-body-language",
            display_name="Emotional Body Language",
            short_description=(
                "Analyzes images where body posture is the primary emotional signal using de Gelder's "
                "emotional body language framework — bodily expressions are automatically perceived and "
                "coupled to action readiness — then maps posture-emotion into VA."
            ),
            theory_family="emotional-body-language",
            selection_hints=[
                "body posture or gesture is the primary emotional content, face is absent or secondary",
                "the image shows silhouettes, distant figures, masked/helmeted subjects, or back-turned bodies",
                "posture conveys recognizable action readiness: freeze, flee, approach, attack, collapse",
            ],
            use_when=(
                "Use when body posture is the dominant emotional channel and the face is absent, obscured, "
                "or secondary. Do not use when a clear face dominates (Todorov or Cognitive Appraisal)."
            ),
            image_signals=[
                "expanded or contracted body configuration",
                "limb positioning indicating tension, openness, or protection",
                "forward lean (approach/aggression) or recoil (fear/avoidance)",
                "postural energy level: high (tense, explosive) vs low (slack, collapsed)",
                "spatial orientation and body direction relative to viewer",
            ],
            va_focus=(
                "Map body posture to emotion category (fear, anger, sadness, joy, dominance, submission), "
                "then derive VA from the category and postural energy. Gaze direction is a modifier layer: "
                "direct gaze adds A +0.2-0.4."
            ),
            analysis_steps=[
                "confirm body posture is the primary emotional signal, not a readable face",
                "describe visible body configuration: expansion/contraction, limb position, tension",
                "map configuration to emotion category and action readiness",
                "assess postural energy level to determine arousal",
                "apply gaze modifier if gaze direction is detectable, then estimate final VA",
            ],
        ),
        PsychologySkillSpec(
            skill_id="awe",
            display_name="Awe",
            short_description=(
                "Analyzes images depicting vast, grand, or sublime stimuli using Keltner & Haidt's awe "
                "framework — perceived vastness and need for accommodation — with both positive awe "
                "(safe vastness → wonder) and threat-based awe (dangerous vastness → overwhelm), then maps into VA."
            ),
            theory_family="awe",
            selection_hints=[
                "the image conveys immense scale, grandeur, or vastness that dwarfs the viewer",
                "towering mountains, star-filled skies, massive architecture, volcanic eruptions, vast canyons",
                "the viewer's likely response is awe, wonder, feeling small, or being overwhelmed by scale",
            ],
            use_when=(
                "Use when the image's dominant affective content is perceived vastness or grandeur. "
                "Do not use for calm gentle nature (Kaplan ART) or for novelty/complexity-driven aesthetics (Berlyne)."
            ),
            image_signals=[
                "extreme size disparity between human scale and environment",
                "unbounded horizon or infinite extension",
                "vertical immensity: towering peaks, cathedral vaults, deep canyons",
                "atmospheric depth cues and diminishing scale",
                "threat-vastness cues: natural disaster, extreme height, uncontrollable force",
            ],
            va_focus=(
                "Dual-branch mapping: safe vastness → V positive, A high (wonder/self-transcendence); "
                "threatening vastness → V negative, A very high (overwhelm/terror-tinged sublimity). "
                "Awe is always high arousal; low arousal scenes are Kaplan ART territory."
            ),
            analysis_steps=[
                "apply three-way routing test: is this Awe (vastness), ART (calm/restorative), or Berlyne (novelty/complexity)?",
                "describe visible vastness cues: scale disparity, extension, depth, human references",
                "assess whether vastness is safe/beautiful or threatening/dangerous",
                "estimate self-diminishment strength from scale references",
                "estimate VA using the dual-branch mapping: safe-awe or threat-awe",
            ],
        ),
    ]
