from __future__ import annotations

from .mapping_tables import PANAS_DISCRETE_VA_MAP
from .schemas import PsychologySkillSpec


def build_default_skill_specs() -> list[PsychologySkillSpec]:
    return [
        PsychologySkillSpec(
            skill_id="panas-discrete-va",
            display_name="PANAS Discrete Emotion VA",
            short_description="Matches the image to PANAS discrete affect terms and aggregates VA from an explicit mapping table.",
            theory_family="panas-discrete-to-va",
            selection_hints=[
                "discrete emotion words can be reasonably inferred from expression and scene",
                "the task asks for affect labels before VA estimation",
                "the user mentions PANAS, PNAS, positive affect, or negative affect",
            ],
            use_when=(
                "Use when you want the model to first infer which PANAS affect "
                "adjectives best match the image, then estimate final VA from the "
                "configured discrete-emotion mapping table."
            ),
            image_signals=[
                "facial expression",
                "body activation level",
                "approach or avoidance cues",
                "goal engagement cues",
                "stress or tension markers",
            ],
            va_focus=(
                "Estimate valence and arousal by weighting matched PANAS discrete "
                "emotions and aggregating their mapped VA coordinates."
            ),
            analysis_steps=[
                "extract visible affective cues from face, body, and context",
                "rank the most plausible PANAS affect adjectives",
                "assign weights to the matched discrete emotions",
                "aggregate mapped VA coordinates into the final estimate",
                "explain uncertainty and competing emotion hypotheses",
            ],
            discrete_emotions=list(PANAS_DISCRETE_VA_MAP.keys()),
            emotion_va_map=PANAS_DISCRETE_VA_MAP,
            aggregation_rule=(
                "Use a weighted average over the configured PANAS emotion->VA map. "
                "Prefer 2 to 5 matched emotions and normalize weights to sum to 1."
            ),
        ),
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
    ]
