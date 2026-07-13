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
    "Use one shared 1-9 scoring scale for every skill and direct baseline:\n"
    "Score valence on 1-9: 1 = very negative/unpleasant, 3 = clearly unpleasant, 5 = neutral, 7 = clearly pleasant, 9 = very positive.\n"
    "Score arousal on 1-9 as viewer ACTIVATION, never as importance, meaning, or image detail:\n"
    "- 1-2: static, empty, or sleepy content.\n"
    "- 3-4: ordinary calm content. Most everyday objects, buildings, landscapes, posed or neutral people, and routine activities belong in this band.\n"
    "- 5-6: clearly engaging or active content: visible sport action, lively social energy, strong emotional displays.\n"
    "- 7-8: imminent threat, violence, explicit erotica, extreme action or force in motion.\n"
    "- 9: immediate extreme danger or shock.\n"
    "Arousal evidence gate: score arousal above 4.5 only when you can cite at least one concrete visible activation cue: "
    "motion/action, imminent threat or close threatening proximity, interpersonal conflict or passion, uncontrollable force, or an intense facial/body display. "
    "Negative meaning, disgust, sadness, seriousness, visual complexity, and rich detail are NOT activation cues. "
    "With no activation cue, arousal_score must be <= 4.5.\n"
    "Always include a top-level activation_evidence array listing those concrete cues; use [] when there are none.\n"
    "In a typical mixed image set roughly half of all images belong below 5.0 arousal; defaulting most images to 5 or higher "
    "is a known bias, so check the 3-4 band first for calm content.\n"
    "Score with one decimal of precision (for example 3.5, 4.2, 6.8); do not snap every score to 5.0, 6.0, or 7.0.\n"
    "Judge VA only after completing the skill's observable inference procedure. Do not convert a semantic label directly into a score.\n"
    "Reserve scores near 1 or 9 for multiple converging, unambiguous visible cues; keep weak or conflicting evidence closer to the center.\n"
    "The top-level JSON keys valence_score and arousal_score are mandatory in every analysis response. "
    "Never omit them; if evidence is weak or ambiguous, still provide your best estimate and explain uncertainty.\n"
    "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
    "Do not put VA scores only inside nested objects such as scores, va, final_va, or analysis. "
    "Do not use alternate names such as final_valence, final_arousal, valence, arousal, or VA TENDENCY as the only score fields.\n"
    "Keep the JSON compact: at most 5 visual_evidence items, 4 construct_estimates, 3 context_modifiers, and 3 activation_evidence items.\n"
)


FULL_INFERENCE_VA_SCORE_INSTRUCTIONS = (
    "Use one shared 1-9 scoring scale for every skill and direct baseline:\n"
    "Score valence on 1-9: 1 = very negative/unpleasant, 3 = clearly unpleasant, 5 = neutral, 7 = clearly pleasant, 9 = very positive.\n"
    "Score arousal on 1-9 as viewer ACTIVATION, never as importance, meaning, or image detail: "
    "1-2 static/empty; 3-4 ordinary calm content (most everyday objects, landscapes, posed or neutral people, routine activity); "
    "5-6 clearly engaging or active content; 7-8 imminent threat, violence, explicit erotica, extreme action; 9 immediate extreme danger.\n"
    "Arousal evidence gate: score arousal above 4.5 only with at least one concrete visible activation cue "
    "(motion/action, imminent threat or close proximity, interpersonal conflict or passion, uncontrollable force, intense facial/body display). "
    "Negative meaning, disgust, sadness, seriousness, complexity, and detail are NOT activation cues; with no activation cue, arousal_score must be <= 4.5.\n"
    "Always include a top-level activation_evidence array with those concrete cues; use [] when there are none.\n"
    "Roughly half of a typical mixed image set belongs below 5.0 arousal; check the 3-4 band first for calm content.\n"
    "Score with one decimal of precision (for example 3.5, 4.2, 6.8); do not snap every score to 5.0, 6.0, or 7.0.\n"
    "Judge VA only after the observable inference procedure and reserve extreme scores for converging evidence.\n"
    "The top-level JSON keys valence_score and arousal_score are mandatory in every analysis response. "
    "Never omit them; if evidence is weak or ambiguous, still provide your best estimate and explain uncertainty.\n"
    "Return only valence_score and arousal_score for the numeric VA values. Do not return normalized 0-1 valence/arousal; the script will normalize later.\n"
    "Do not put VA scores only inside nested objects such as scores, va, final_va, or analysis. "
    "Do not use alternate names such as final_valence, final_arousal, valence, arousal, or VA TENDENCY as the only score fields.\n"
    "For explanatory fields, provide a bounded structured rationale based on visible evidence and the selected model. "
    "Do not expose private hidden chain-of-thought; provide an auditable summary of observations, construct estimates, modifiers, and the final VA judgment.\n"
)


def _catalog_as_text(skill_specs: list[PsychologySkillSpec]) -> str:
    rows = []
    for spec in skill_specs:
        if not spec.routing_enabled:
            continue
        routing_card = spec.routing_card or {
            "use_when": spec.selection_hints[:3] or ([spec.use_when] if spec.use_when else []),
            "visual_triggers": spec.image_signals[:6],
            "routing_priority": spec.analysis_steps[:2],
        }
        rows.append(
            {
                "skill_id": spec.skill_id,
                "display_name": spec.display_name,
                "applicability_gate": {key: value for key, value in routing_card.items() if value},
            }
        )
    return json.dumps(rows, ensure_ascii=True, indent=2)


def _routing_preference_rules() -> str:
    return (
        "- Decision order (check top to bottom; the FIRST clear match wins):\n"
        "  1. evolved-fear-module: a snake, spider, scorpion, or large predator is the dominant content.\n"
        "  2. pathogen-disgust: visible contamination, rot, mutilation, wounds, bodily waste, or infestation dominates.\n"
        "  3. baby-schema: an infant, baby animal, or clearly neotenic character is the dominant subject.\n"
        "  4. facial-expression-affect: a clear EXPRESSIVE human face dominates (visible smile, laughter, crying, anger, fear) "
        "with readable brow/eye plus mouth/jaw regions; partial, hand-distorted, neutral, or ambiguous faces do not qualify.\n"
        "  5. emotional-body-language: body posture or action carries the emotion and the face is absent, small, or unreadable.\n"
        "  6. awe: physically overwhelming scale with reliable scale references dominates.\n"
        "  7. kaplan-art-restoration: an enterable, calm, low-demand environment dominates.\n"
        "  8. berlyne-arousal-pleasure: artwork, design, or abstract composition where perceptual complexity, novelty, or incongruity itself drives affect.\n"
        "  9. cognitive-appraisal: a visible consequential EVENT (attack, accident, rescue, embrace, intimacy, achievement, violation) "
        "with visible stakes and at least two evidence-supported appraisal dimensions.\n"
        "  10. Otherwise no_specialized_skill.\n"
        "- Humans being present is NOT a reason to pick cognitive-appraisal. Buying, eating, waiting, posing, standing, working, "
        "gathering, or socializing without a visible consequential change is no_specialized_skill.\n"
        "- Neutral or mildly expressive portraits without a clear transient expression are no_specialized_skill, "
        "not facial-expression-affect and not cognitive-appraisal.\n"
        "- no_specialized_skill is the correct answer for roughly one third of typical mixed images; "
        "choosing it is a successful routing decision, not a failure.\n"
    )


def build_routing_system_prompt(skill_specs: list[PsychologySkillSpec]) -> str:
    return (
        "You are a psychology-model router for visual affect analysis.\n"
        f"{VA_AFFECT_DEFINITION}\n"
        "Choose one specialized psychology skill only when its applicability gate strongly matches the image.\n"
        f"If no specialized skill strongly matches, return skill_id={NO_SPECIALIZED_SKILL_ID} and candidate_skill_ids=[].\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Each skill includes one compact applicability gate. Match visible mechanisms, not emotion words or scene labels.\n"
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
        "Choose one specialized psychology skill only when its applicability gate strongly matches the image.\n"
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
        '  "selected_valence_score": 5.0,\n'
        '  "selected_arousal_score": 5.0,\n'
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


def _skill_specific_analysis_contract(skill_id: str) -> tuple[str, str]:
    if skill_id != "facial-expression-affect":
        return "", ""
    instructions = (
        "Facial-expression-specific mandatory contract:\n"
        "- Report face_reliability as observable booleans. Do not guess a hidden mouth/jaw region.\n"
        "- external_distortion is true when a hand/object presses, covers, or visibly deforms a diagnostic region.\n"
        "- Report viewer_transfer separately from depicted expression intensity. Missing body/event/context is an attenuator, not confirmation.\n"
        "- Set gate_decision=use_direct unless applicability is strong, brow/eye and mouth/jaw are both reliable, external_distortion is false, and viewer transfer is supported.\n"
    )
    schema_fields = (
        '  "face_reliability": {"face_clear": true, "brow_eye_visible": true, '
        '"mouth_jaw_visible": true, "external_distortion": false},\n'
        '  "viewer_transfer": {"level":"low|medium|high", "amplifiers":[], "attenuators":[]},\n'
        '  "gate_decision": "use_skill|use_direct",\n'
    )
    return instructions, schema_fields


def build_analysis_system_prompt(skill_spec: PsychologySkillSpec) -> str:
    skill_specific_instructions, skill_specific_schema = _skill_specific_analysis_contract(
        skill_spec.skill_id
    )
    compact_skill_definition = {
        "skill_id": skill_spec.skill_id,
        "display_name": skill_spec.display_name,
        "short_description": skill_spec.short_description,
        "theory_family": skill_spec.theory_family,
        "applicability_gate": skill_spec.routing_card,
        "image_signals": skill_spec.image_signals,
        "va_focus": skill_spec.va_focus,
        "analysis_steps": skill_spec.analysis_steps,
        "worked_example": skill_spec.worked_example,
    }
    return (
        "You are a psychology-guided visual affect analyst.\n"
        f"{VA_AFFECT_DEFINITION}"
        "Use the provided skill definition to analyze the image.\n"
        "Follow every numbered inference step in order. Each construct estimate must cite visible evidence.\n"
        "Always include applicability: strong, partial, or weak. If weak, keep scores conservative and explain the mismatch.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Do not copy the skill's narrative output template. Convert the analysis into the JSON schema below.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{VA_SCORE_INSTRUCTIONS}"
        f"{skill_specific_instructions}"
        f"Skill definition:\n{json.dumps(compact_skill_definition, ensure_ascii=True, indent=2)}\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.0,\n'
        '  "arousal_score": 5.0,\n'
        '  "skill_id": "skill-id",\n'
        '  "quadrant": "short label",\n'
        '  "applicability": "strong|partial|weak",\n'
        f"{skill_specific_schema}"
        '  "activation_evidence": ["concrete visible activation cue; [] if none"],\n'
        '  "summary": "concise explanation",\n'
        '  "visual_evidence": [{"variable":"skill variable","observation":"visible fact","level":"low|medium|high"}],\n'
        '  "construct_estimates": [{"construct":"theory construct","level":"low|medium|high","basis":"visible evidence"}],\n'
        '  "context_modifiers": ["visible modifier or competing mechanism"],\n'
        '  "evidence": ["most score-relevant visible cue"],\n'
        '  "uncertainty": "brief uncertainty note",\n'
        '  "inference_summary": "concise progression from evidence to constructs to VA"\n'
        "}\n"
    )


def build_full_skill_analysis_system_prompt(skill_spec: PsychologySkillSpec) -> str:
    skill_specific_instructions, skill_specific_schema = _skill_specific_analysis_contract(
        skill_spec.skill_id
    )
    compact_skill_definition = {
        "skill_id": skill_spec.skill_id,
        "display_name": skill_spec.display_name,
        "short_description": skill_spec.short_description,
        "theory_family": skill_spec.theory_family,
        "applicability_gate": skill_spec.routing_card,
        "image_signals": skill_spec.image_signals,
        "va_focus": skill_spec.va_focus,
        "analysis_steps": skill_spec.analysis_steps,
        "worked_example": skill_spec.worked_example,
    }
    raw_skill_markdown = skill_spec.raw_skill_markdown or ""
    return (
        "You are a psychology-guided visual affect analyst.\n"
        f"{VA_AFFECT_DEFINITION}"
        "This is a full-skill utilization trace run. Use the selected skill's complete SKILL.md, not only its compact summary.\n"
        "Apply the skill's applicability gate, visual variables, inference procedure, VA judgment, and worked example to the visible image evidence. "
        "When a skill construct is weak or not applicable, state that briefly instead of forcing the image to fit the theory.\n"
        "Always include an applicability field: strong, partial, or weak. If applicability is weak, still output top-level VA scores, but make them conservative and explain the scope mismatch instead of pretending the skill fits.\n"
        "Return exactly one valid JSON object and no Markdown, no code fences, no headings, no prose before or after the JSON.\n"
        "Do not copy the skill's narrative output template. Convert the analysis into the JSON schema below.\n"
        "The first two top-level keys of the object must be valence_score and arousal_score.\n"
        f"{FULL_INFERENCE_VA_SCORE_INSTRUCTIONS}"
        f"{skill_specific_instructions}"
        f"Compact skill metadata:\n{json.dumps(compact_skill_definition, ensure_ascii=True, indent=2)}\n\n"
        f"Full SKILL.md:\n{raw_skill_markdown}\n\n"
        "Required JSON schema:\n"
        "{\n"
        '  "valence_score": 5.0,\n'
        '  "arousal_score": 5.0,\n'
        '  "skill_id": "skill-id",\n'
        '  "quadrant": "short label",\n'
        '  "applicability": "strong|partial|weak",\n'
        f"{skill_specific_schema}"
        '  "activation_evidence": ["concrete visible activation cue; [] if none"],\n'
        '  "summary": "concise final affect summary",\n'
        '  "visual_evidence": [{"variable":"skill variable","observation":"visible fact","level":"low|medium|high"}],\n'
        '  "evidence": ["visible cue used for scoring"],\n'
        '  "construct_estimates": [{"construct":"skill construct","level":"low|medium|high","basis":"visible evidence"}],\n'
        '  "skill_procedure_trace": ["step-by-step application of the selected skill to the image"],\n'
        '  "context_modifiers": ["visible modifier or competing mechanism"],\n'
        '  "va_judgment": "how evidence and constructs support final V and A without a hard lookup table",\n'
        '  "uncertainty": "uncertainty and limitations",\n'
        '  "inference_summary": "auditable evidence-to-construct-to-VA summary"\n'
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
        '  "valence_score": 5.0,\n'
        '  "arousal_score": 5.0,\n'
        '  "quadrant": "short label",\n'
        '  "activation_evidence": ["concrete visible activation cue; [] if none"],\n'
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
        '  "valence_score": 5.0,\n'
        '  "arousal_score": 5.0,\n'
        '  "quadrant": "short label",\n'
        '  "activation_evidence": ["concrete visible activation cue; [] if none"],\n'
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
