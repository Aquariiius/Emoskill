from __future__ import annotations

import json

from .schemas import NO_SPECIALIZED_SKILL_ID, PsychologySkillSpec


VA_AFFECT_DEFINITION = (
    "Basic affective VA definition:\n"
    "- Valence measures affective pleasantness: negative/unpleasant -> neutral -> positive/pleasant.\n"
    "- Arousal measures activation, energy, and intensity independently from valence: calm/deactivated -> moderate activation -> highly activated.\n"
    "- Do not collapse arousal into positivity: excitement and fear can both be high-arousal; peace and boredom can both be low-arousal.\n"
    "- Arousal is not the same as visual complexity or salience: a highly detailed but calm scene (e.g. an intricate but peaceful garden) is not automatically high-arousal.\n"
    "- Base the estimate on visible image evidence, and state uncertainty when the evidence is weak or ambiguous.\n"
)


VA_SCORE_INSTRUCTIONS = (
    "Use this 1-10 scoring scale for numeric VA outputs:\n"
    "Score valence on a 1-10 scale: 1 = very negative/unpleasant, 5.5 = neutral, 10 = very positive/pleasant.\n"
    "Score arousal on a 1-10 scale: 1 = very calm/deactivated, 5.5 = moderate activation, 10 = highly activated. "
    "Note that 5.5 on arousal means 'moderate activation', not 'neutral' — arousal has no true neutral point the way valence does.\n"
    "The top-level JSON keys valence_score and arousal_score are mandatory in every analysis response. "
    "Never omit them; if evidence is weak or ambiguous, still provide your best estimate and explain uncertainty.\n"
    "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
    "Do not put VA scores only inside nested objects such as scores, va, final_va, or analysis. "
    "Do not use alternate names such as final_valence, final_arousal, valence, arousal, or VA TENDENCY as the only score fields.\n"
    "Keep the full JSON compact enough to finish within the token budget: use at most 3 evidence items, "
    "at most 3 mapping_trace items, at most 3 observed_cues, and make reasoning_trace a single short string under 35 words.\n"
)


FULL_INFERENCE_VA_SCORE_INSTRUCTIONS = (
    "Use this 1-10 scoring scale for numeric VA outputs:\n"
    "Score valence on a 1-10 scale: 1 = very negative/unpleasant, 5.5 = neutral, 10 = very positive/pleasant.\n"
    "Score arousal on a 1-10 scale: 1 = very calm/deactivated, 5.5 = moderate activation, 10 = highly activated.\n"
    "The top-level JSON keys valence_score and arousal_score are mandatory in every analysis response. "
    "Never omit them; if evidence is weak or ambiguous, still provide your best estimate and explain uncertainty.\n"
    "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
    "Do not put VA scores only inside nested objects such as scores, va, final_va, or analysis. "
    "Do not use alternate names such as final_valence, final_arousal, valence, arousal, or VA TENDENCY as the only score fields.\n"
    "For explanatory fields, provide a detailed but bounded structured rationale based on visible evidence and the selected model. "
    "Do not expose private hidden chain-of-thought; instead provide an auditable inference summary with observations, applied constructs, and VA mapping.\n"
)


def _catalog_as_text(skill_specs: list[PsychologySkillSpec]) -> str:
    rows = []
    for spec in skill_specs:
        routing_card = spec.routing_card or {
            "use_when": spec.selection_hints[:3] or ([spec.use_when] if spec.use_when else []),
            "visual_triggers": spec.image_signals[:6],
            "routing_priority": spec.analysis_steps[:2],
        }
        rows.append(
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "short_description": _compact_text(spec.short_description, max_chars=160),
                "routing_card": {key: value for key, value in routing_card.items() if value},
            }
        )
    return json.dumps(rows, ensure_ascii=True, indent=2)


def _compact_text(text: str, *, max_chars: int) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."


def _routing_preference_rules() -> str:
    return (
        "- Prefer kaplan-art-restoration for restorative environments, especially nature and recovery-oriented scenes.\n"
        "- Prefer berlyne-arousal-pleasure for artworks, design, novelty, complexity, and aesthetic stimulation.\n"
        "- Prefer todorov-face-evaluation when a human face is central and the judgment depends on trustworthiness or dominance impressions.\n"
        "- Prefer cognitive-appraisal when the affect depends on inferred goals, agency, responsibility, coping potential, or situational meaning.\n"
        "- Prefer evolved-fear-module when evolutionarily threatening animals (snakes, spiders, predators) are the dominant content.\n"
        "- Prefer pathogen-disgust for visible contamination, rot, bodily waste, wounds, or pest infestation.\n"
        "- Prefer baby-schema when an infant, baby animal, or neotenic character is the dominant subject.\n"
        "- Prefer emotional-body-language when human body posture or gesture carries the primary emotional signal and the face is obscured or secondary.\n"
        "- Prefer awe when the scene depicts grand, majestic, or vast scale (towering mountains, star skies, storm systems).\n"
    )


def build_routing_system_prompt(skill_specs: list[PsychologySkillSpec]) -> str:
    return (
        "You are a psychology-model router for visual affect analysis.\n"
        f"{VA_AFFECT_DEFINITION}\n"
        "Choose one specialized psychology skill only when a routing card strongly matches the image.\n"
        f"If no specialized skill strongly matches, return skill_id={NO_SPECIALIZED_SKILL_ID} and candidate_skill_ids=[].\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Each skill includes a compact routing card. Use it as the first-pass selector and match only visible cue structure.\n"
        "Available skills:\n"
        f"{_catalog_as_text(skill_specs)}\n\n"
        "Rules:\n"
        "- Base your decision on visible evidence first.\n"
        "- Use user context only as a secondary hint.\n"
        f"{_routing_preference_rules()}"
        "- If the image is ambiguous but no specialized skill is clearly activated, choose no_specialized_skill rather than forcing a weak match.\n"
        "- candidate_skill_ids is an at-most list, not a quota. Do not pad it.\n"
        "- Usually include exactly 1 candidate. Include 2 only for a real boundary case. Use [] when no specialized skill fits.\n"
        "- A candidate is strongly plausible only if its core constructs are directly visible, not merely loosely related.\n"
        "- Confidence must be in [0, 1].\n"
        "- Keep reason under 25 words, observed_cues to at most 3 items, and alternative_skill_ids to at most 2 items.\n"
        "Required JSON schema: "
        '{"skill_id":"skill-id-or-no_specialized_skill","reason":"brief reason","confidence":0.0,'
        '"observed_cues":["cue"],"candidate_skill_ids":["skill-id","other-skill-id"],'
        '"alternative_skill_ids":["other-skill-id"]}\n'
    )


def build_full_routing_system_prompt(skill_specs: list[PsychologySkillSpec]) -> str:
    return (
        "You are a psychology-model router for visual affect analysis.\n"
        f"{VA_AFFECT_DEFINITION}\n"
        "Choose one specialized psychology skill only when a routing card strongly matches the image.\n"
        f"If no specialized skill strongly matches, return skill_id={NO_SPECIALIZED_SKILL_ID} and candidate_skill_ids=[].\n"
        "This is a long-form inference trace run: explain the routing decision with enough detail to audit why this skill was selected.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Available skills:\n"
        f"{_catalog_as_text(skill_specs)}\n\n"
        "Rules:\n"
        "- Base your decision on visible evidence first.\n"
        "- Use user context only as a secondary hint.\n"
        f"{_routing_preference_rules()}"
        "- Prefer the model whose theoretical constructs are most directly activated by the visible scene.\n"
        "- If the image is ambiguous but no specialized skill is clearly activated, explain that and choose no_specialized_skill rather than forcing a weak match.\n"
        "- candidate_skill_ids is an at-most list, not a quota. Do not pad it.\n"
        "- Usually include exactly 1 candidate. Include 2 only for a real boundary case. Use [] when no specialized skill fits.\n"
        "- A candidate is strongly plausible only if its core constructs are directly visible, not merely loosely related.\n"
        "- Confidence must be in [0, 1].\n"
        "Required JSON schema:\n"
        "{\n"
        '  "skill_id": "skill-id-or-no_specialized_skill",\n'
        '  "reason": "one-sentence final routing decision",\n'
        '  "confidence": 0.0,\n'
        '  "observed_cues": ["visible cue"],\n'
        '  "candidate_skill_ids": ["skill-id", "other-skill-id"],\n'
        '  "visual_skill_match": ["how a visible cue matches a skill construct"],\n'
        '  "selection_reasoning": "detailed evidence-based rationale for the selected skill",\n'
        '  "alternative_skill_ids": ["other-skill-id"],\n'
        '  "rejected_alternatives": [{"skill_id": "other-skill-id", "why_not": "brief reason"}],\n'
        '  "uncertainty": "brief routing uncertainty note"\n'
        "}\n"
    )


def build_routing_user_prompt(user_context: str) -> str:
    return (
        "Select one specialized psychology skill for this image only if it strongly fits; otherwise select no_specialized_skill.\n"
        f"User context: {user_context or 'None provided.'}"
    )


def build_skill_selection_system_prompt(candidate_skill_ids: list[str]) -> str:
    return (
        "You are a final arbiter for psychology-guided visual affect analysis.\n"
        f"{VA_AFFECT_DEFINITION}\n"
        "You will receive several candidate skill analyses for the same image. "
        "Choose the single candidate whose psychology model is best matched to the visible evidence and whose VA score is most justified.\n"
        "Do not average the candidates and do not invent a new score. Select one candidate's score as final.\n"
        "Penalize candidates that force a weak or inapplicable skill onto the image, even if their VA score sounds plausible or extreme.\n"
        "Prefer a slightly less dramatic score from a correctly scoped skill over an impressive score from a scope mismatch.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        f"Allowed candidate_skill_ids: {json.dumps(candidate_skill_ids, ensure_ascii=True)}\n"
        "Required JSON schema:\n"
        "{\n"
        '  "selected_skill_id": "skill-id",\n'
        '  "reason": "why this candidate is the best final score source",\n'
        '  "selected_valence_score": 5.5,\n'
        '  "selected_arousal_score": 5.5,\n'
        '  "rejected_candidates": [{"skill_id": "other-skill-id", "why_not": "brief reason"}],\n'
        '  "confidence": 0.0\n'
        "}\n"
    )


def build_skill_selection_user_prompt(
    *,
    route: dict,
    candidate_analyses: list[dict],
    user_context: str,
) -> str:
    payload = {
        "route": route,
        "candidate_analyses": candidate_analyses,
        "user_context": user_context or "None provided.",
    }
    return (
        "Choose the best final skill analysis for this image from the candidate analyses below. "
        "Select one candidate's existing score; do not synthesize a new VA score.\n"
        f"{json.dumps(payload, ensure_ascii=True, indent=2)}"
    )


def build_analysis_system_prompt(skill_spec: PsychologySkillSpec) -> str:
    compact_skill_definition = {
        "skill_id": skill_spec.skill_id,
        "display_name": skill_spec.display_name,
        "short_description": skill_spec.short_description,
        "theory_family": skill_spec.theory_family,
        "selection_hints": skill_spec.selection_hints,
        "use_when": skill_spec.use_when,
        "image_signals": skill_spec.image_signals,
        "va_focus": skill_spec.va_focus,
        "analysis_steps": skill_spec.analysis_steps,
        "discrete_emotions": skill_spec.discrete_emotions,
        "emotion_va_map": skill_spec.emotion_va_map,
        "aggregation_rule": skill_spec.aggregation_rule,
    }
    return (
        "You are a psychology-guided visual affect analyst.\n"
        f"{VA_AFFECT_DEFINITION}"
        "Use the provided skill definition to analyze the image.\n"
        "Always include an applicability field: strong, partial, or weak. If applicability is weak, still output top-level VA scores, but make them conservative and explain the scope mismatch instead of pretending the skill fits.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Do not copy the skill's narrative output template. Convert the analysis into the JSON schema below.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{VA_SCORE_INSTRUCTIONS}"
        f"Skill definition:\n{json.dumps(compact_skill_definition, ensure_ascii=True, indent=2)}\n\n"
        "If the selected skill includes discrete_emotions and emotion_va_map, you must:\n"
        "- first identify 2 to 5 most plausible discrete emotions from that list\n"
        "- assign normalized weights summing to 1\n"
        "- estimate final valence_score and arousal_score from the weighted mapping table, which also uses 1-10 scores\n"
        "- include the mapping process in the output\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.5,\n'
        '  "arousal_score": 5.5,\n'
        '  "skill_id": "skill-id",\n'
        '  "quadrant": "short label",\n'
        '  "applicability": "strong|partial|weak",\n'
        '  "summary": "concise explanation",\n'
        '  "evidence": ["visible cue"],\n'
        '  "matched_emotions": ["emotion term"],\n'
        '  "emotion_weights": {"emotion term": 1.0},\n'
        '  "mapping_trace": ["mapping step"],\n'
        '  "appraisal_notes": ["inferred appraisal note"],\n'
        '  "positive_affect": ["likely positive affect state"],\n'
        '  "negative_affect": ["likely negative affect state"],\n'
        '  "uncertainty": "brief uncertainty note",\n'
        '  "observed_cues": ["cue"],\n'
        '  "reasoning_trace": "one concise sentence, not a list"\n'
        "}\n"
    )


def build_full_skill_analysis_system_prompt(skill_spec: PsychologySkillSpec) -> str:
    compact_skill_definition = {
        "skill_id": skill_spec.skill_id,
        "display_name": skill_spec.display_name,
        "short_description": skill_spec.short_description,
        "theory_family": skill_spec.theory_family,
        "selection_hints": skill_spec.selection_hints,
        "use_when": skill_spec.use_when,
        "image_signals": skill_spec.image_signals,
        "va_focus": skill_spec.va_focus,
        "analysis_steps": skill_spec.analysis_steps,
        "discrete_emotions": skill_spec.discrete_emotions,
        "emotion_va_map": skill_spec.emotion_va_map,
        "aggregation_rule": skill_spec.aggregation_rule,
    }
    raw_skill_markdown = skill_spec.raw_skill_markdown or ""
    return (
        "You are a psychology-guided visual affect analyst.\n"
        f"{VA_AFFECT_DEFINITION}"
        "This is a full-skill utilization trace run. Use the selected skill's complete SKILL.md, not only its compact summary.\n"
        "Apply the skill's named constructs, use-when rules, reasoning steps, mapping principles, and output guidance to the visible image evidence. "
        "When a skill construct is weak or not applicable, state that briefly instead of forcing the image to fit the theory.\n"
        "Always include an applicability field: strong, partial, or weak. If applicability is weak, still output top-level VA scores, but make them conservative and explain the scope mismatch instead of pretending the skill fits.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Do not copy the skill's narrative output template. Convert the analysis into the JSON schema below.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{FULL_INFERENCE_VA_SCORE_INSTRUCTIONS}"
        f"Compact skill metadata:\n{json.dumps(compact_skill_definition, ensure_ascii=True, indent=2)}\n\n"
        f"Full SKILL.md:\n{raw_skill_markdown}\n\n"
        "If the selected skill includes discrete_emotions and emotion_va_map, you must:\n"
        "- identify 2 to 5 most plausible discrete emotions from that list\n"
        "- assign normalized weights summing to 1\n"
        "- estimate final valence_score and arousal_score from the weighted mapping table, which also uses 1-10 scores\n"
        "- include the mapping process in the output\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.5,\n'
        '  "arousal_score": 5.5,\n'
        '  "skill_id": "skill-id",\n'
        '  "quadrant": "short label",\n'
        '  "applicability": "strong|partial|weak",\n'
        '  "summary": "concise final affect summary",\n'
        '  "visual_observations": ["specific visible cue"],\n'
        '  "evidence": ["visible cue used for scoring"],\n'
        '  "skill_constructs_applied": [{"construct": "skill construct", "image_evidence": "visible cue", "effect_on_va": "VA implication"}],\n'
        '  "skill_procedure_trace": ["step-by-step application of the selected skill to the image"],\n'
        '  "matched_emotions": ["emotion term"],\n'
        '  "emotion_weights": {"emotion term": 1.0},\n'
        '  "mapping_trace": ["mapping step"],\n'
        '  "va_mapping_reasoning": "detailed explanation of how the skill evidence maps to final valence_score and arousal_score",\n'
        '  "appraisal_notes": ["inferred appraisal note"],\n'
        '  "positive_affect": ["likely positive affect state"],\n'
        '  "negative_affect": ["likely negative affect state"],\n'
        '  "uncertainty": "uncertainty and limitations",\n'
        '  "observed_cues": ["cue"],\n'
        '  "reasoning_trace": "auditable rationale, 4-8 sentences, grounded in the selected skill and visible image evidence"\n'
        "}\n"
    )


def build_analysis_user_prompt(
    skill_id: str,
    route_reason: str,
    user_context: str,
) -> str:
    return (
        "Analyze this image with the selected psychology model.\n"
        f"Selected skill_id: {skill_id}\n"
        f"Routing reason: {route_reason}\n"
        f"User context: {user_context or 'None provided.'}"
    )


def build_direct_va_system_prompt() -> str:
    return (
        "You are a visual affect analyst. Analyze the image directly in valence-arousal space "
        "without using any named psychology skill.\n"
        f"{VA_AFFECT_DEFINITION}"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{VA_SCORE_INSTRUCTIONS}"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.5,\n'
        '  "arousal_score": 5.5,\n'
        '  "quadrant": "short label",\n'
        '  "summary": "concise explanation",\n'
        '  "evidence": ["visible cue"],\n'
        '  "matched_emotions": ["likely emotion or affect term"],\n'
        '  "uncertainty": "brief uncertainty note"\n'
        "}\n"
    )


def build_full_direct_va_system_prompt() -> str:
    return (
        "You are a visual affect analyst. Analyze the image directly in valence-arousal space "
        "without using any named psychology skill.\n"
        f"{VA_AFFECT_DEFINITION}"
        "This is a long-form inference trace run. Provide a detailed but bounded evidence-based rationale for the direct VA baseline.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{FULL_INFERENCE_VA_SCORE_INSTRUCTIONS}"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.5,\n'
        '  "arousal_score": 5.5,\n'
        '  "quadrant": "short label",\n'
        '  "summary": "concise final affect summary",\n'
        '  "visual_observations": ["specific visible cue"],\n'
        '  "evidence": ["visible cue used for scoring"],\n'
        '  "matched_emotions": ["likely emotion or affect term"],\n'
        '  "affect_interpretation": "how the visible cues imply likely affective meaning",\n'
        '  "va_mapping_reasoning": "detailed explanation of how visible evidence maps to final valence_score and arousal_score",\n'
        '  "uncertainty": "uncertainty and limitations",\n'
        '  "reasoning_trace": "auditable rationale, 4-8 sentences, based only on visible image evidence"\n'
        "}\n"
    )


def build_direct_va_user_prompt(user_context: str) -> str:
    return (
        "Analyze this image directly as a VA baseline.\n"
        f"User context: {user_context or 'None provided.'}"
    )
