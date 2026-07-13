from __future__ import annotations

import re
from typing import Any

from .llm_client import MultimodalLLMClient
from .model_catalog import build_default_skill_specs
from .prompts import (
    build_analysis_system_prompt,
    build_analysis_user_prompt,
    build_direct_va_system_prompt,
    build_direct_va_user_prompt,
    build_routing_system_prompt,
    build_routing_user_prompt,
)
from .schemas import (
    MAIN_ROUTING_EXCLUDED_SKILL_IDS,
    NO_SPECIALIZED_SKILL_ID,
    ImageInput,
    PsychologySkillSpec,
    RouteDecision,
    VAAnalysisResult,
)


DEFAULT_FALLBACK_SKILL_PRIORITY = (
    "facial-expression-affect",
    "cognitive-appraisal",
    "emotional-body-language",
    "todorov-face-evaluation",
    "kaplan-art-restoration",
    "berlyne-arousal-pleasure",
    "evolved-fear-module",
    "pathogen-disgust",
    "baby-schema",
    "awe",
)


class PsychologyVAPipeline:
    def __init__(
        self,
        llm_client: MultimodalLLMClient,
        skill_specs: list[PsychologySkillSpec] | None = None,
    ) -> None:
        self.llm_client = llm_client
        self.skill_specs = skill_specs or build_default_skill_specs()
        self.skill_map = {spec.skill_id: spec for spec in self.skill_specs}
        self.routing_skill_specs = [
            spec
            for spec in self.skill_specs
            if spec.routing_enabled and spec.skill_id not in MAIN_ROUTING_EXCLUDED_SKILL_IDS
        ]
        self.routing_skill_map = {spec.skill_id: spec for spec in self.routing_skill_specs}

    def route_skill(self, image_input: ImageInput, user_context: str = "") -> RouteDecision:
        response = self.llm_client.complete_json(
            system_prompt=build_routing_system_prompt(self.routing_skill_specs),
            user_prompt=build_routing_user_prompt(user_context),
            image_payload=image_input.to_llm_payload(),
        )
        return self._normalize_route_decision(response, user_context=user_context)

    def analyze(self, image_input: ImageInput, user_context: str = "") -> VAAnalysisResult:
        route = self.route_skill(image_input=image_input, user_context=user_context)
        return self.analyze_with_route(image_input=image_input, route=route, user_context=user_context)

    def analyze_with_route(
        self,
        image_input: ImageInput,
        route: RouteDecision,
        user_context: str = "",
    ) -> VAAnalysisResult:
        if route.skill_id == NO_SPECIALIZED_SKILL_ID:
            return self.analyze_direct(image_input=image_input, user_context=user_context)

        selected_skill = self.skill_map[route.skill_id]

        response = self.llm_client.complete_json(
            system_prompt=build_analysis_system_prompt(selected_skill),
            user_prompt=build_analysis_user_prompt(
                skill_id=route.skill_id,
                route_reason=route.reason,
                user_context=user_context,
            ),
            image_payload=image_input.to_llm_payload(),
        )
        return self._normalize_analysis_result(selected_skill, response)

    def analyze_direct(self, image_input: ImageInput, user_context: str = "") -> VAAnalysisResult:
        response = self.llm_client.complete_json(
            system_prompt=build_direct_va_system_prompt(),
            user_prompt=build_direct_va_user_prompt(user_context),
            image_payload=image_input.to_llm_payload(),
        )
        direct_spec = PsychologySkillSpec(
            skill_id="direct-va-baseline",
            display_name="Direct VA Baseline",
            short_description="Direct valence-arousal baseline without named psychology skill routing.",
            theory_family="direct-va",
            selection_hints=[],
            use_when="Use as a baseline for comparison against skill-routed VA analysis.",
            image_signals=[],
            va_focus="Directly estimate valence and arousal from visible image cues.",
            analysis_steps=[],
        )
        return self._normalize_analysis_result(direct_spec, response)

    def _normalize_route_decision(
        self,
        payload: dict[str, Any],
        *,
        user_context: str,
    ) -> RouteDecision:
        skill_id = str(payload.get("skill_id") or "").strip()
        candidate_skill_ids = _candidate_skill_ids_from_payload(payload, self.routing_skill_map)
        no_specialized_skill = _is_no_specialized_skill(payload, skill_id)
        if skill_id not in self.routing_skill_map:
            skill_id = (
                candidate_skill_ids[0]
                if candidate_skill_ids and not no_specialized_skill
                else NO_SPECIALIZED_SKILL_ID
            )

        if skill_id == NO_SPECIALIZED_SKILL_ID:
            candidate_skill_ids = []
            alternative_skill_ids: list[str] = []
        else:
            candidate_skill_ids = _dedupe_skill_ids(
                [
                    skill_id,
                    *candidate_skill_ids,
                    *[
                        item
                        for item in _as_string_list(payload.get("alternative_skill_ids"))
                        if item in self.routing_skill_map
                    ],
                ],
                self.routing_skill_map,
            )
            if not candidate_skill_ids:
                candidate_skill_ids = [skill_id]
            alternative_skill_ids = [item for item in candidate_skill_ids if item != skill_id]

        confidence_value = payload.get("confidence", 0.5)
        try:
            confidence = float(confidence_value)
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))

        return RouteDecision(
            skill_id=skill_id,
            reason=str(payload.get("reason") or "No specialized skill strongly matched the visible cue structure."),
            confidence=confidence,
            observed_cues=_as_string_list(payload.get("observed_cues")),
            alternative_skill_ids=alternative_skill_ids,
            candidate_skill_ids=candidate_skill_ids,
        )

    def _normalize_analysis_result(
        self,
        skill_spec: PsychologySkillSpec,
        payload: dict[str, Any],
    ) -> VAAnalysisResult:
        payload = _normalize_analysis_payload(payload)
        if skill_spec.skill_id != "direct-va-baseline":
            _validate_skill_inference_payload(payload, skill_id=skill_spec.skill_id)
        payload = _apply_arousal_evidence_gate(payload)
        valence_score = _required_float_in_range(payload, "valence_score", low=1.0, high=9.0)
        arousal_score = _required_float_in_range(payload, "arousal_score", low=1.0, high=9.0)
        valence = _score_to_unit_interval(valence_score)
        arousal = _score_to_unit_interval(arousal_score)

        return VAAnalysisResult(
            skill_id=skill_spec.skill_id,
            skill_name=skill_spec.display_name,
            valence=valence,
            arousal=arousal,
            quadrant=str(payload.get("quadrant") or _infer_quadrant(valence_score, arousal_score)),
            summary=str(payload.get("summary") or "No summary returned by the model."),
            evidence=_as_string_list(payload.get("evidence")),
            matched_emotions=_as_string_list(payload.get("matched_emotions")),
            emotion_weights=_as_float_dict(payload.get("emotion_weights")),
            mapping_trace=_as_string_list(payload.get("mapping_trace")),
            appraisal_notes=_as_string_list(payload.get("appraisal_notes")),
            positive_affect=_as_string_list(payload.get("positive_affect")),
            negative_affect=_as_string_list(payload.get("negative_affect")),
            uncertainty=str(payload.get("uncertainty") or ""),
            applicability=str(payload.get("applicability") or ""),
            activation_evidence=_as_string_list(payload.get("activation_evidence")),
            visual_evidence=_as_dict_list(payload.get("visual_evidence")),
            construct_estimates=_as_dict_list(payload.get("construct_estimates")),
            context_modifiers=_as_string_list(payload.get("context_modifiers")),
            inference_summary=str(payload.get("inference_summary") or ""),
            raw_model_output=payload,
            valence_score=valence_score,
            arousal_score=arousal_score,
        )

    def _fallback_skill_id(self, user_context: str) -> str:
        hint = user_context.lower()
        if (
            "appraisal" in hint
            or "social context" in hint
            or "scenario" in hint
            or "achievement" in hint
            or "stress" in hint
            or "frustration" in hint
        ):
            return self._first_available(["cognitive-appraisal"])
        if (
            "attention restoration" in hint
            or "restoration" in hint
            or "restorative" in hint
            or "nature" in hint
            or "landscape" in hint
        ):
            return self._first_available(["kaplan-art-restoration", "awe", "berlyne-arousal-pleasure"])
        if (
            "berlyne" in hint
            or "aesthetic" in hint
            or "aesthetics" in hint
            or "novelty" in hint
            or "complexity" in hint
            or "artwork" in hint
            or "design" in hint
        ):
            return self._first_available(["berlyne-arousal-pleasure", "awe"])
        if "todorov" in hint or "trustworthiness" in hint or "facial dominance" in hint:
            return self._first_available(["todorov-face-evaluation"])
        if (
            "face" in hint
            or "facial" in hint
            or "portrait" in hint
            or "smile" in hint
            or "frown" in hint
            or "expression" in hint
        ):
            return self._first_available(["facial-expression-affect", "cognitive-appraisal"])
        if (
            "snake" in hint
            or "spider" in hint
            or "predator" in hint
            or "fear module" in hint
            or "phobia" in hint
            or "evolved fear" in hint
        ):
            return self._first_available(["evolved-fear-module", "cognitive-appraisal"])
        if (
            "disgust" in hint
            or "pathogen" in hint
            or "contamination" in hint
            or "rot" in hint
            or "decay" in hint
            or "wound" in hint
            or "infestation" in hint
        ):
            return self._first_available(["pathogen-disgust", "cognitive-appraisal"])
        if (
            "baby" in hint
            or "infant" in hint
            or "cute" in hint
            or "cuteness" in hint
            or "kindchenschema" in hint
            or "neotenic" in hint
            or "kawaii" in hint
        ):
            return self._first_available(["baby-schema", "cognitive-appraisal"])
        if (
            "body language" in hint
            or "body posture" in hint
            or "posture" in hint
            or "silhouette" in hint
            or "gesture" in hint
            or "de gelder" in hint
        ):
            return self._first_available(["emotional-body-language", "cognitive-appraisal"])
        if (
            "awe" in hint
            or "vastness" in hint
            or "sublime" in hint
            or "grandeur" in hint
            or "overwhelming scale" in hint
            or "majestic" in hint
        ):
            return self._first_available(["awe", "kaplan-art-restoration"])
        return self._first_available(list(DEFAULT_FALLBACK_SKILL_PRIORITY))

    def _first_available(self, skill_ids: list[str]) -> str:
        for skill_id in skill_ids:
            if skill_id in self.skill_map:
                return skill_id
        return next(iter(self.skill_map))


def _candidate_skill_ids_from_payload(
    payload: dict[str, Any],
    skill_map: dict[str, PsychologySkillSpec],
) -> list[str]:
    raw_items: list[Any] = []
    for key in ("candidate_skill_ids", "candidate_skills", "skill_ids", "alternative_skill_ids"):
        value = payload.get(key)
        if isinstance(value, list):
            raw_items.extend(value)
        elif isinstance(value, str):
            raw_items.extend(value.replace(",", " ").split())

    for value in payload.get("rejected_alternatives") or []:
        if isinstance(value, dict):
            raw_items.append(value.get("skill_id"))
        else:
            raw_items.append(value)

    return _dedupe_skill_ids([str(item).strip() for item in raw_items if item], skill_map)


def _is_no_specialized_skill(payload: dict[str, Any], skill_id: str) -> bool:
    normalized_skill_id = _normalize_key(skill_id)
    if normalized_skill_id in {
        _normalize_key(NO_SPECIALIZED_SKILL_ID),
        "noskill",
        "none",
        "directva",
        "directvabaseline",
    }:
        return True

    for key in ("no_specialized_skill", "no_skill", "use_direct_va"):
        value = payload.get(key)
        if isinstance(value, bool) and value:
            return True
        if isinstance(value, str) and value.strip().lower() in {"true", "yes", "1"}:
            return True
    return False


def _dedupe_skill_ids(
    skill_ids: list[str],
    skill_map: dict[str, PsychologySkillSpec],
) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for skill_id in skill_ids:
        if skill_id not in skill_map or skill_id in seen:
            continue
        deduped.append(skill_id)
        seen.add(skill_id)
    return deduped


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_analysis_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError(f"Model output must be a JSON object, got {type(payload).__name__}")

    normalized = dict(payload)
    recovery_notes: list[str] = []

    for score_key in ("valence_score", "arousal_score"):
        if score_key not in normalized:
            recovered = _find_score_value(payload, score_key)
            if recovered is not None:
                normalized[score_key] = recovered
                recovery_notes.append(f"{score_key}:alias_or_nested")

    if "valence_score" not in normalized or "arousal_score" not in normalized:
        text = _payload_text(payload)
        valence_score, arousal_score = _extract_va_scores_from_text(text)
        if "valence_score" not in normalized and valence_score is not None:
            normalized["valence_score"] = valence_score
            recovery_notes.append("valence_score:text")
        if "arousal_score" not in normalized and arousal_score is not None:
            normalized["arousal_score"] = arousal_score
            recovery_notes.append("arousal_score:text")

    if recovery_notes:
        normalized["_parse_recovery"] = ",".join(recovery_notes)

    return normalized


AROUSAL_EVIDENCE_GATE_ENABLED = True
AROUSAL_EVIDENCE_GATE_CAP = 4.5


def _apply_arousal_evidence_gate(payload: dict[str, Any]) -> dict[str, Any]:
    """Cap arousal when the model itself reports no visible activation cue.

    Fires only when activation_evidence is present AND empty, so legacy outputs
    that omit the field are never modified. The adjustment is recorded in the
    payload (_arousal_gate) so gated samples stay countable and auditable.
    """
    if not AROUSAL_EVIDENCE_GATE_ENABLED:
        return payload
    value = payload.get("activation_evidence")
    if not isinstance(value, list):
        return payload
    cues = [str(item).strip() for item in value if str(item).strip()]
    if cues:
        return payload
    try:
        arousal = float(payload.get("arousal_score"))
    except (TypeError, ValueError):
        return payload
    if arousal <= AROUSAL_EVIDENCE_GATE_CAP:
        return payload
    adjusted = dict(payload)
    adjusted["arousal_score"] = AROUSAL_EVIDENCE_GATE_CAP
    adjusted["_arousal_gate"] = (
        f"arousal {arousal} capped to {AROUSAL_EVIDENCE_GATE_CAP}: empty activation_evidence"
    )
    return adjusted


def _validate_skill_inference_payload(payload: dict[str, Any], *, skill_id: str = "") -> None:
    applicability = str(payload.get("applicability") or "").strip().lower()
    if applicability not in {"strong", "partial", "weak"}:
        raise ValueError("Skill output must include applicability: strong, partial, or weak")

    visual_evidence = payload.get("visual_evidence")
    if not isinstance(visual_evidence, list) or not visual_evidence:
        raise ValueError("Skill output must include non-empty visual_evidence")

    construct_estimates = payload.get("construct_estimates")
    if not isinstance(construct_estimates, list) or not construct_estimates:
        raise ValueError("Skill output must include non-empty construct_estimates")

    inference_summary = payload.get("inference_summary")
    if not isinstance(inference_summary, str) or not inference_summary.strip():
        raise ValueError("Skill output must include a non-empty inference_summary")

    if skill_id == "facial-expression-affect":
        reliability = payload.get("face_reliability")
        if not isinstance(reliability, dict):
            raise ValueError("Facial expression output must include face_reliability")
        for key in (
            "face_clear",
            "brow_eye_visible",
            "mouth_jaw_visible",
            "external_distortion",
        ):
            if not isinstance(reliability.get(key), bool):
                raise ValueError(f"face_reliability.{key} must be boolean")

        viewer_transfer = payload.get("viewer_transfer")
        if not isinstance(viewer_transfer, dict):
            raise ValueError("Facial expression output must include viewer_transfer")
        if str(viewer_transfer.get("level") or "").strip().lower() not in {
            "low",
            "medium",
            "high",
        }:
            raise ValueError("viewer_transfer.level must be low, medium, or high")

        gate_decision = str(payload.get("gate_decision") or "").strip().lower()
        if gate_decision not in {"use_skill", "use_direct"}:
            raise ValueError("Facial expression output must include gate_decision: use_skill or use_direct")


def _find_score_value(payload: dict[str, Any], score_key: str) -> float | None:
    target = "valence" if score_key == "valence_score" else "arousal"
    direct_aliases = {
        f"{target}_score",
        f"{target} score",
        f"{target}score",
        f"{target}_rating",
        f"{target} rating",
        f"{target}_value",
        f"{target} value",
        f"final_{target}",
        f"final {target}",
        f"final_{target}_score",
        f"final {target} score",
    }

    value = _value_for_alias(payload, direct_aliases)
    if value is not None:
        parsed = _score_from_value(value)
        if parsed is not None:
            return parsed

    for nested_key in (
        "scores",
        "score",
        "va",
        "va_scores",
        "va_score",
        "final_va",
        "final_va_scores",
        "valence_arousal",
        "affect",
        "result",
        "analysis",
        "output",
    ):
        nested = _value_for_alias(payload, {nested_key})
        if not isinstance(nested, dict):
            continue
        value = _value_for_alias(nested, direct_aliases | {target})
        if value is None and isinstance(nested.get(target), dict):
            value = _value_for_alias(nested[target], {"score", "value", "rating"})
        parsed = _score_from_value(value)
        if parsed is not None:
            return parsed

    plain_value = _value_for_alias(payload, {target})
    parsed = _score_from_value(plain_value, allow_unit_interval=True)
    if parsed is not None:
        return parsed
    return None


def _value_for_alias(payload: dict[str, Any], aliases: set[str]) -> Any:
    normalized_aliases = {_normalize_key(alias) for alias in aliases}
    for key, value in payload.items():
        if _normalize_key(str(key)) in normalized_aliases:
            return value
    return None


def _normalize_key(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", key.lower())


def _score_from_value(value: Any, *, allow_unit_interval: bool = False) -> float | None:
    if isinstance(value, dict):
        value = _value_for_alias(value, {"score", "value", "rating"})
    if value is None or isinstance(value, (list, tuple)):
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", str(value))
        if not numbers:
            return None
        parsed = float(numbers[0])
    if 1.0 <= parsed <= 9.0:
        return parsed
    if allow_unit_interval and 0.0 <= parsed <= 1.0:
        return round((parsed * 8.0) + 1.0, 6)
    return None


def _payload_text(value: Any) -> str:
    chunks: list[str] = []

    def visit(item: Any) -> None:
        if isinstance(item, str):
            chunks.append(item)
        elif isinstance(item, dict):
            for nested in item.values():
                visit(nested)
        elif isinstance(item, list):
            for nested in item:
                visit(nested)

    visit(value)
    return "\n".join(chunks)


def _extract_va_scores_from_text(text: str) -> tuple[float | None, float | None]:
    if not text:
        return None, None

    valence_score = _score_from_labeled_text(text, "valence")
    arousal_score = _score_from_labeled_text(text, "arousal")
    return valence_score, arousal_score


def _score_from_labeled_text(text: str, label: str) -> float | None:
    patterns = [
        rf"\bfinal\s+{label}(?:\s+score)?\s*[:=]\s*([^\n\r,;|]+)",
        rf"\b{label}(?:\s+score)?\s*[:=]\s*([^\n\r,;|]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        parsed = _score_from_value(match.group(1))
        if parsed is not None:
            return parsed
    return None


def _required_float_in_range(payload: dict[str, Any], key: str, *, low: float, high: float) -> float:
    if key not in payload:
        keys = ", ".join(str(item) for item in payload.keys())
        raise ValueError(f"Model output missing required key: {key}; available keys: [{keys}]")
    try:
        value = float(payload[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Model output key {key!r} must be numeric, got {payload[key]!r}") from exc
    if value < low or value > high:
        raise ValueError(f"Model output key {key!r}={value} outside expected range [{low}, {high}]")
    return value


def _score_to_unit_interval(score: float) -> float:
    return round((score - 1.0) / 8.0, 6)


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _as_string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


def _as_float_dict(value: Any) -> dict[str, float]:
    if not isinstance(value, dict):
        return {}

    result: dict[str, float] = {}
    for key, item in value.items():
        try:
            result[str(key)] = float(item)
        except (TypeError, ValueError):
            continue
    return result


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _infer_quadrant(valence: float, arousal: float) -> str:
    valence_label = "positive" if valence > 5.0 else "negative" if valence < 5.0 else "neutral"
    arousal_label = "high-arousal" if arousal > 5.0 else "low-arousal" if arousal < 5.0 else "moderate-arousal"
    return f"{arousal_label} {valence_label}"
