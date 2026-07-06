from __future__ import annotations

import json

from .schemas import PsychologySkillSpec


def _catalog_as_text(skill_specs: list[PsychologySkillSpec]) -> str:
    rows = []
    for spec in skill_specs:
        rows.append(
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "short_description": spec.short_description,
                "theory_family": spec.theory_family,
                "selection_hints": spec.selection_hints,
                "use_when": spec.use_when,
                "image_signals": spec.image_signals,
                "va_focus": spec.va_focus,
                "analysis_steps": spec.analysis_steps,
            }
        )
    return json.dumps(rows, ensure_ascii=True, indent=2)


def build_routing_system_prompt(skill_specs: list[PsychologySkillSpec]) -> str:
    return (
        "You are a psychology-model router for visual affect analysis.\n"
        "Choose the single best psychology skill for the image.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Each skill includes a short description and selection hints. Use them as the first-pass selector, then confirm with use_when and visible cues.\n"
        "Available skills:\n"
        f"{_catalog_as_text(skill_specs)}\n\n"
        "Rules:\n"
        "- Base your decision on visible evidence first.\n"
        "- Use user context only as a secondary hint.\n"
        "- Prefer panas-discrete-va when PANAS-style discrete affect words can be grounded from the image.\n"
        "- Prefer kaplan-art-restoration for restorative environments, especially nature and recovery-oriented scenes.\n"
        "- Prefer berlyne-arousal-pleasure for artworks, design, novelty, complexity, and aesthetic stimulation.\n"
        "- Prefer todorov-face-evaluation when a human face is central and the judgment depends on trustworthiness or dominance impressions.\n"
        "- If the image is ambiguous, choose the model whose visible cue structure best matches the scene rather than inventing unsupported theory claims.\n"
        "- Confidence must be in [0, 1].\n"
        'Required JSON schema: {"skill_id":"skill-id","reason":"brief reason","confidence":0.0,"observed_cues":["cue"],"alternative_skill_ids":["other-skill-id"]}\n'
    )


def build_routing_user_prompt(user_context: str) -> str:
    return (
        "Select the best psychology skill for this image.\n"
        f"User context: {user_context or 'None provided.'}"
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
        "Use the provided skill definition to analyze the image.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Do not copy the skill's narrative output template. Convert the analysis into the JSON schema below.\n"
        "Score valence on a 1-10 scale: 1 = very negative, 5.5 = neutral, 10 = very positive.\n"
        "Score arousal on a 1-10 scale: 1 = very calm/deactivated, 5.5 = moderate activation, 10 = highly activated.\n"
        "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
        f"Skill definition:\n{json.dumps(compact_skill_definition, ensure_ascii=True, indent=2)}\n\n"
        "If the selected skill includes discrete_emotions and emotion_va_map, you must:\n"
        "- first identify 2 to 5 most plausible discrete emotions from that list\n"
        "- assign normalized weights summing to 1\n"
        "- estimate final valence_score and arousal_score from the weighted mapping table, which also uses 1-10 scores\n"
        "- include the mapping process in the output\n"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.5,\n'
        '  "arousal_score": 5.5,\n'
        '  "quadrant": "short label",\n'
        '  "summary": "concise explanation",\n'
        '  "evidence": ["visible cue"],\n'
        '  "matched_emotions": ["emotion term"],\n'
        '  "emotion_weights": {"emotion term": 1.0},\n'
        '  "mapping_trace": ["mapping step"],\n'
        '  "appraisal_notes": ["inferred appraisal note"],\n'
        '  "positive_affect": ["likely positive affect state"],\n'
        '  "negative_affect": ["likely negative affect state"],\n'
        '  "uncertainty": "short uncertainty note"\n'
        "}\n"
    )


def build_analysis_user_prompt(skill_id: str, route_reason: str, user_context: str) -> str:
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
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Score valence on a 1-10 scale: 1 = very negative, 5.5 = neutral, 10 = very positive.\n"
        "Score arousal on a 1-10 scale: 1 = very calm/deactivated, 5.5 = moderate activation, 10 = highly activated.\n"
        "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
        "Output keys:\n"
        "- valence_score: number in [1, 10]\n"
        "- arousal_score: number in [1, 10]\n"
        "- quadrant: short label\n"
        "- summary: concise explanation\n"
        "- evidence: list of visible cues\n"
        "- matched_emotions: list of likely emotion or affect terms\n"
        "- uncertainty: short uncertainty note\n"
    )


def build_direct_va_user_prompt(user_context: str) -> str:
    return (
        "Analyze this image directly as a VA baseline.\n"
        f"User context: {user_context or 'None provided.'}"
    )
