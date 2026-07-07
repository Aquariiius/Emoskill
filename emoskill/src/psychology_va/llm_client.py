from __future__ import annotations

import base64
import copy
import io
import json
import re
from pathlib import Path
from typing import Any, Protocol


class MultimodalLLMClient(Protocol):
    """Contract for a multimodal model client used by the VA pipeline."""

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        image_payload: dict[str, Any],
    ) -> dict[str, Any]:
        """Return a parsed JSON object from a multimodal model."""


class ModelOutputParseError(ValueError):
    """Raised when a model response cannot be converted into the expected object."""

    def __init__(self, message: str, *, raw_text: str, parse_error: Exception | None = None) -> None:
        super().__init__(message)
        self.raw_text = raw_text
        self.parse_error = parse_error


class Qwen25VLClient:
    """Local/server-side Qwen2.5-VL client backed by transformers."""

    def __init__(
        self,
        *,
        model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct",
        device_map: str | dict[str, Any] = "auto",
        torch_dtype: str = "auto",
        max_new_tokens: int = 512,
        trust_remote_code: bool = True,
    ) -> None:
        self.model_name = model_name
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        self.max_new_tokens = max_new_tokens
        self.trust_remote_code = trust_remote_code
        self._model = None
        self._processor = None
        self.last_raw_output_text = ""

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        image_payload: dict[str, Any],
    ) -> dict[str, Any]:
        self._ensure_loaded()

        image = self._load_image(image_payload)
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": user_prompt},
                ],
            },
        ]

        prompt_text = self._processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._processor(
            text=[prompt_text],
            images=[image],
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self._model.device)

        output_ids = self._model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
        )
        generated_ids = output_ids[:, inputs.input_ids.shape[1] :]
        output_text = self._processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )[0]
        self.last_raw_output_text = output_text
        return _extract_json_object(output_text)

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._processor is not None:
            return

        try:
            from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
        except ImportError as exc:
            raise ImportError(
                "Qwen25VLClient requires `transformers` with Qwen2.5-VL support installed."
            ) from exc

        model_kwargs: dict[str, Any] = {
            "device_map": self.device_map,
            "trust_remote_code": self.trust_remote_code,
        }
        if self.torch_dtype != "auto":
            try:
                import torch
            except ImportError as exc:
                raise ImportError("Qwen25VLClient requires `torch` installed.") from exc

            if not hasattr(torch, self.torch_dtype):
                raise ValueError(f"Unsupported torch dtype: {self.torch_dtype}")
            model_kwargs["torch_dtype"] = getattr(torch, self.torch_dtype)
        else:
            model_kwargs["torch_dtype"] = "auto"

        self._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            self.model_name,
            **model_kwargs,
        )
        self._processor = AutoProcessor.from_pretrained(
            self.model_name,
            trust_remote_code=self.trust_remote_code,
        )

    def _load_image(self, image_payload: dict[str, Any]) -> Any:
        try:
            from PIL import Image
        except ImportError as exc:
            raise ImportError("Qwen25VLClient requires `Pillow` installed.") from exc

        image_path = image_payload.get("image_path")
        image_url = image_payload.get("image_url")
        image_b64 = image_payload.get("image_b64")

        if image_path:
            return Image.open(Path(image_path)).convert("RGB")
        if image_url:
            try:
                import requests
            except ImportError as exc:
                raise ImportError("Image URL input requires `requests` installed.") from exc

            response = requests.get(str(image_url), timeout=30)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content)).convert("RGB")
        if image_b64:
            raw_bytes = base64.b64decode(image_b64)
            return Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        raise ValueError("ImageInput must provide image_path, image_url, or image_b64.")


class Qwen3VLClient:
    """Local/server-side Qwen3-VL client backed by transformers."""

    def __init__(
        self,
        *,
        model_name: str = "/home/u1120250383/dyp/models/qwen",
        device_map: str | dict[str, Any] = "auto",
        dtype: str = "auto",
        max_new_tokens: int = 512,
        min_pixels: int | None = None,
        max_pixels: int | None = 1003520,
        trust_remote_code: bool = True,
    ) -> None:
        self.model_name = model_name
        self.device_map = device_map
        self.dtype = dtype
        self.max_new_tokens = max_new_tokens
        self.min_pixels = min_pixels
        self.max_pixels = max_pixels
        self.trust_remote_code = trust_remote_code
        self._model = None
        self._processor = None
        self.last_raw_output_text = ""

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        image_payload: dict[str, Any],
    ) -> dict[str, Any]:
        self._ensure_loaded()

        try:
            import torch
            from qwen_vl_utils import process_vision_info
        except ImportError as exc:
            raise ImportError("Qwen3VLClient requires `torch` and `qwen_vl_utils` installed.") from exc

        image_ref = self._image_reference(image_payload)
        combined_prompt = f"{system_prompt.strip()}\n\n{user_prompt.strip()}"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image_ref},
                    {"type": "text", "text": combined_prompt},
                ],
            }
        ]

        prompt_text = self._processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self._processor(
            text=[prompt_text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(_get_input_device(self._model))

        generate_kwargs: dict[str, Any] = {
            "max_new_tokens": self.max_new_tokens,
            "do_sample": False,
        }
        generation_config = _deterministic_generation_config(self._model)
        if generation_config is not None:
            generate_kwargs["generation_config"] = generation_config
        with torch.inference_mode():
            output_ids = self._model.generate(**inputs, **generate_kwargs)
        generated_ids = [
            output_ids_item[len(input_ids_item) :]
            for input_ids_item, output_ids_item in zip(inputs.input_ids, output_ids)
        ]
        output_text = self._processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )[0]
        self.last_raw_output_text = output_text
        return _extract_json_object(output_text)

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._processor is not None:
            return

        try:
            import transformers
            from transformers import AutoProcessor
        except ImportError as exc:
            raise ImportError("Qwen3VLClient requires `transformers` installed.") from exc

        model_class = getattr(transformers, "Qwen3VLForConditionalGeneration", None)
        if model_class is None:
            raise ImportError(
                "Qwen3VLClient requires transformers with Qwen3VLForConditionalGeneration support."
            )

        model_kwargs: dict[str, Any] = {
            "device_map": self.device_map,
            "trust_remote_code": self.trust_remote_code,
        }
        self._model = _from_pretrained_with_auto_dtype(
            model_class,
            self.model_name,
            dtype=self.dtype,
            **model_kwargs,
        ).eval()

        processor_kwargs: dict[str, Any] = {"trust_remote_code": self.trust_remote_code}
        if self.min_pixels is not None:
            processor_kwargs["min_pixels"] = self.min_pixels
        if self.max_pixels is not None:
            processor_kwargs["max_pixels"] = self.max_pixels
        self._processor = AutoProcessor.from_pretrained(self.model_name, **processor_kwargs)

    def _image_reference(self, image_payload: dict[str, Any]) -> str:
        image_path = image_payload.get("image_path")
        image_url = image_payload.get("image_url")
        image_b64 = image_payload.get("image_b64")
        mime_type = image_payload.get("mime_type") or "image/png"

        if image_path:
            return str(Path(image_path).expanduser())
        if image_url:
            return str(image_url)
        if image_b64:
            return f"data:{mime_type};base64,{image_b64}"
        raise ValueError("ImageInput must provide image_path, image_url, or image_b64.")


class StubMultimodalLLMClient:
    """Placeholder client kept for compatibility with the original skeleton."""

    def complete_json(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        image_payload: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError(
            "No model client is connected yet. Use Qwen25VLClient for a local/server-side "
            "Qwen2.5-VL deployment, or implement MultimodalLLMClient.complete_json()."
        )


def _extract_json_object(text: str) -> dict[str, Any]:
    candidate = text.strip()
    first_error: json.JSONDecodeError | None = None

    try:
        loaded = json.loads(candidate)
        if isinstance(loaded, dict):
            return loaded
    except json.JSONDecodeError as exc:
        first_error = exc

    for fenced in _iter_fenced_blocks(candidate):
        stripped = fenced.strip()
        if not stripped.startswith("{"):
            continue
        try:
            loaded = json.loads(stripped)
        except json.JSONDecodeError as exc:
            first_error = exc
            continue
        if isinstance(loaded, dict):
            return loaded

    decoder = json.JSONDecoder()
    for index, char in enumerate(candidate):
        if char != "{":
            continue
        try:
            loaded, _ = decoder.raw_decode(candidate[index:])
        except json.JSONDecodeError as exc:
            first_error = exc
            continue
        if isinstance(loaded, dict) and (index == 0 or _looks_like_top_level_object(loaded)):
            return loaded

    recovered = _recover_partial_json_va_object(candidate)
    if recovered is not None:
        return recovered

    recovered = _recover_loose_va_object(candidate)
    if recovered is not None:
        return recovered

    message = f"Model output is not valid JSON: {_preview_text(text)}"
    if first_error is not None:
        message = f"{message} ({first_error})"
    raise ModelOutputParseError(message, raw_text=text, parse_error=first_error)


def _iter_fenced_blocks(text: str) -> list[str]:
    return [
        match.group(1)
        for match in re.finditer(r"```(?:json|JSON)?\s*\n?(.*?)```", text, flags=re.DOTALL)
    ]


def _looks_like_top_level_object(value: dict[str, Any]) -> bool:
    top_level_keys = {
        "valence_score",
        "arousal_score",
        "skill_id",
        "reason",
        "confidence",
        "quadrant",
        "summary",
        "evidence",
        "observed_cues",
        "alternative_skill_ids",
    }
    return bool(top_level_keys.intersection(value.keys()))


def _recover_partial_json_va_object(text: str) -> dict[str, Any] | None:
    valence_score = _json_number_for_key(text, "valence_score")
    arousal_score = _json_number_for_key(text, "arousal_score")
    if valence_score is None or arousal_score is None:
        return None

    return {
        "valence_score": valence_score,
        "arousal_score": arousal_score,
        "skill_id": _json_string_for_key(text, "skill_id") or "",
        "quadrant": _json_string_for_key(text, "quadrant") or _infer_recovered_quadrant(valence_score, arousal_score),
        "summary": _json_string_for_key(text, "summary") or _first_nonempty_line(text),
        "evidence": [],
        "matched_emotions": [],
        "emotion_weights": {},
        "mapping_trace": [],
        "appraisal_notes": [],
        "positive_affect": [],
        "negative_affect": [],
        "uncertainty": "Recovered from truncated JSON model output; inspect raw_model_output for details.",
        "_parse_recovery": "partial_json_scores",
        "_raw_text": text,
    }


def _json_number_for_key(text: str, key: str) -> float | None:
    match = re.search(
        rf'"{re.escape(key)}"\s*:\s*([+-]?\d+(?:\.\d+)?)',
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def _json_string_for_key(text: str, key: str) -> str:
    match = re.search(
        rf'"{re.escape(key)}"\s*:\s*"((?:\\.|[^"\\])*)"',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return ""
    try:
        return json.loads(f'"{match.group(1)}"')
    except json.JSONDecodeError:
        return match.group(1)


def _recover_loose_va_object(text: str) -> dict[str, Any] | None:
    valence_text: str | None = None
    arousal_text: str | None = None

    final_valence = re.search(
        r"FINAL\s+VALENCE(?:\s+SCORE)?\s*:\s*([^\n\r|]+)",
        text,
        flags=re.IGNORECASE,
    )
    final_arousal = re.search(
        r"FINAL\s+AROUSAL(?:\s+SCORE)?\s*:\s*([^\n\r|]+)",
        text,
        flags=re.IGNORECASE,
    )
    if final_valence and final_arousal:
        valence_text = final_valence.group(1)
        arousal_text = final_arousal.group(1)
    else:
        tendency = re.search(
            r"VA\s+TENDENCY\s*:\s*Valence(?:\s+Score)?\s*:\s*([^,\n\r|]+),\s*Arousal(?:\s+Score)?\s*:\s*([^\n\r|]+)",
            text,
            flags=re.IGNORECASE,
        )
        if tendency:
            valence_text = tendency.group(1)
            arousal_text = tendency.group(2)

    valence_score = _parse_numeric_or_range(valence_text)
    arousal_score = _parse_numeric_or_range(arousal_text)
    if valence_score is None or arousal_score is None:
        return None

    return {
        "valence_score": valence_score,
        "arousal_score": arousal_score,
        "quadrant": _infer_recovered_quadrant(valence_score, arousal_score),
        "summary": _first_nonempty_line(text),
        "evidence": [],
        "matched_emotions": [],
        "emotion_weights": {},
        "mapping_trace": [],
        "appraisal_notes": [],
        "positive_affect": [],
        "negative_affect": [],
        "uncertainty": "Recovered from non-JSON model text; inspect raw_model_output for details.",
        "_parse_recovery": "loose_va_text",
        "_raw_text": text,
    }


def _parse_numeric_or_range(value: str | None) -> float | None:
    if not value:
        return None
    numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", value)
    if not numbers:
        return None
    parsed = [float(item) for item in numbers[:2]]
    if len(parsed) == 2 and "to" in value.lower():
        return sum(parsed) / 2
    return parsed[0]


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip("` \t")
        if stripped:
            return stripped[:500]
    return "Recovered from non-JSON model output."


def _infer_recovered_quadrant(valence: float, arousal: float) -> str:
    valence_label = "positive" if valence > 5.5 else "negative" if valence < 5.5 else "neutral"
    arousal_label = "high-arousal" if arousal > 5.5 else "low-arousal" if arousal < 5.5 else "moderate-arousal"
    return f"{arousal_label} {valence_label}"


def _preview_text(text: str, limit: int = 1200) -> str:
    compact = text.strip()
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "... [truncated]"


def _deterministic_generation_config(model: Any) -> Any | None:
    generation_config = getattr(model, "generation_config", None)
    if generation_config is None:
        return None

    generation_config = copy.deepcopy(generation_config)
    generation_config.do_sample = False
    for name in ("temperature", "top_p", "top_k"):
        if hasattr(generation_config, name):
            setattr(generation_config, name, None)
    return generation_config


def _get_input_device(model: Any) -> str:
    hf_device_map = getattr(model, "hf_device_map", None)
    if isinstance(hf_device_map, dict):
        for value in hf_device_map.values():
            if isinstance(value, int):
                return f"cuda:{value}"
            if isinstance(value, str) and value.startswith("cuda"):
                return value

    model_device = getattr(model, "device", None)
    if model_device is not None and str(model_device) != "meta":
        return str(model_device)

    try:
        import torch

        if torch.cuda.is_available():
            return "cuda:0"
    except Exception:
        pass
    return "cpu"


def _from_pretrained_with_auto_dtype(model_class: Any, model_name: str, *, dtype: str, **kwargs: Any) -> Any:
    attempts: list[dict[str, Any]]
    if dtype == "auto":
        attempts = [{"dtype": "auto"}, {"torch_dtype": "auto"}, {}]
    else:
        try:
            import torch
        except ImportError as exc:
            raise ImportError("A non-auto dtype requires `torch` installed.") from exc

        if not hasattr(torch, dtype):
            raise ValueError(f"Unsupported torch dtype: {dtype}")
        torch_dtype = getattr(torch, dtype)
        attempts = [{"dtype": torch_dtype}, {"torch_dtype": torch_dtype}, {}]

    last_error: Exception | None = None
    for dtype_kwargs in attempts:
        try:
            return model_class.from_pretrained(model_name, **dtype_kwargs, **kwargs)
        except TypeError as exc:
            last_error = exc
            if "torch_dtype" not in str(exc) and "dtype" not in str(exc):
                raise
        except Exception:
            raise
    if last_error is not None:
        raise last_error
    raise RuntimeError("from_pretrained failed without an exception")
