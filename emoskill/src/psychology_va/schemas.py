from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


NO_SPECIALIZED_SKILL_ID = "no_specialized_skill"
MAIN_ROUTING_EXCLUDED_SKILL_IDS = frozenset({"todorov-face-evaluation"})


@dataclass(frozen=True)
class PsychologySkillSpec:
    skill_id: str
    display_name: str
    short_description: str
    theory_family: str
    selection_hints: list[str]
    use_when: str
    image_signals: list[str]
    va_focus: str
    analysis_steps: list[str]
    routing_card: dict[str, list[str]] = field(default_factory=dict)
    discrete_emotions: list[str] = field(default_factory=list)
    emotion_va_map: dict[str, dict[str, float]] = field(default_factory=dict)
    aggregation_rule: str = ""
    source_path: str = ""
    raw_skill_markdown: str = ""
    worked_example: str = ""
    routing_enabled: bool = True


@dataclass(frozen=True)
class ImageInput:
    image_url: str | None = None
    image_path: str | None = None
    image_b64: str | None = None
    mime_type: str | None = None

    def to_llm_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.image_url:
            payload["image_url"] = self.image_url
        if self.image_path:
            payload["image_path"] = self.image_path
        if self.image_b64:
            payload["image_b64"] = self.image_b64
        if self.mime_type:
            payload["mime_type"] = self.mime_type
        return payload


@dataclass
class RouteDecision:
    skill_id: str
    reason: str
    confidence: float
    observed_cues: list[str] = field(default_factory=list)
    alternative_skill_ids: list[str] = field(default_factory=list)
    candidate_skill_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VAAnalysisResult:
    skill_id: str
    skill_name: str
    valence: float
    arousal: float
    quadrant: str
    summary: str
    evidence: list[str] = field(default_factory=list)
    matched_emotions: list[str] = field(default_factory=list)
    emotion_weights: dict[str, float] = field(default_factory=dict)
    mapping_trace: list[str] = field(default_factory=list)
    appraisal_notes: list[str] = field(default_factory=list)
    positive_affect: list[str] = field(default_factory=list)
    negative_affect: list[str] = field(default_factory=list)
    uncertainty: str = ""
    applicability: str = ""
    visual_evidence: list[dict[str, Any]] = field(default_factory=list)
    construct_estimates: list[dict[str, Any]] = field(default_factory=list)
    context_modifiers: list[str] = field(default_factory=list)
    inference_summary: str = ""
    raw_model_output: dict[str, Any] = field(default_factory=dict)
    valence_score: float | None = None
    arousal_score: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
