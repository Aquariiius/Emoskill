from __future__ import annotations

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
from .schemas import ImageInput, PsychologySkillSpec, RouteDecision, VAAnalysisResult


class PsychologyVAPipeline:
    def __init__(
        self,
        llm_client: MultimodalLLMClient,
        skill_specs: list[PsychologySkillSpec] | None = None,
    ) -> None:
        self.llm_client = llm_client
        self.skill_specs = skill_specs or build_default_skill_specs()
        self.skill_map = {spec.skill_id: spec for spec in self.skill_specs}

    def route_skill(self, image_input: ImageInput, user_context: str = "") -> RouteDecision:
        response = self.llm_client.complete_json(
            system_prompt=build_routing_system_prompt(self.skill_specs),
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
        if skill_id not in self.skill_map:
            skill_id = self._fallback_skill_id(user_context)

        confidence_value = payload.get("confidence", 0.5)
        try:
            confidence = float(confidence_value)
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))

        return RouteDecision(
            skill_id=skill_id,
            reason=str(payload.get("reason") or "Fallback route based on default policy."),
            confidence=confidence,
            observed_cues=_as_string_list(payload.get("observed_cues")),
            alternative_skill_ids=[
                item for item in _as_string_list(payload.get("alternative_skill_ids")) if item in self.skill_map
            ],
        )

    def _normalize_analysis_result(
        self,
        skill_spec: PsychologySkillSpec,
        payload: dict[str, Any],
    ) -> VAAnalysisResult:
        valence_score = _required_float_in_range(payload, "valence_score", low=1.0, high=10.0)
        arousal_score = _required_float_in_range(payload, "arousal_score", low=1.0, high=10.0)
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
            raw_model_output=payload,
            valence_score=valence_score,
            arousal_score=arousal_score,
        )

    def _fallback_skill_id(self, user_context: str) -> str:
        hint = user_context.lower()
        if "panas" in hint or "pnas" in hint or "positive affect" in hint or "negative affect" in hint:
            return self._first_available(["panas-discrete-va", "panas-affect-profile", "core-affect-va"])
        if (
            "appraisal" in hint
            or "social context" in hint
            or "scenario" in hint
            or "achievement" in hint
            or "stress" in hint
            or "frustration" in hint
        ):
            return self._first_available(["cognitive-appraisal", "core-affect-va", "panas-discrete-va"])
        if (
            "attention restoration" in hint
            or "restoration" in hint
            or "restorative" in hint
            or "nature" in hint
            or "landscape" in hint
        ):
            return self._first_available(["kaplan-art-restoration", "core-affect-va"])
        if (
            "berlyne" in hint
            or "aesthetic" in hint
            or "aesthetics" in hint
            or "novelty" in hint
            or "complexity" in hint
            or "artwork" in hint
            or "design" in hint
        ):
            return self._first_available(["berlyne-arousal-pleasure", "core-affect-va"])
        if (
            "todorov" in hint
            or "face" in hint
            or "facial" in hint
            or "portrait" in hint
            or "trustworthiness" in hint
            or "dominance" in hint
        ):
            return self._first_available(["todorov-face-evaluation", "core-affect-va"])
        return self._first_available(["core-affect-va", "panas-discrete-va"])

    def _first_available(self, skill_ids: list[str]) -> str:
        for skill_id in skill_ids:
            if skill_id in self.skill_map:
                return skill_id
        return next(iter(self.skill_map))


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _required_float_in_range(payload: dict[str, Any], key: str, *, low: float, high: float) -> float:
    if key not in payload:
        raise ValueError(f"Model output missing required key: {key}")
    try:
        value = float(payload[key])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Model output key {key!r} must be numeric, got {payload[key]!r}") from exc
    if value < low or value > high:
        raise ValueError(f"Model output key {key!r}={value} outside expected range [{low}, {high}]")
    return value


def _score_to_unit_interval(score: float) -> float:
    return round((score - 1.0) / 9.0, 6)


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


def _infer_quadrant(valence: float, arousal: float) -> str:
    valence_label = "positive" if valence > 5.5 else "negative" if valence < 5.5 else "neutral"
    arousal_label = "high-arousal" if arousal > 5.5 else "low-arousal" if arousal < 5.5 else "moderate-arousal"
    return f"{arousal_label} {valence_label}"
