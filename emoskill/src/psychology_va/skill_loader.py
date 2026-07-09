from __future__ import annotations

import re
from pathlib import Path

from .schemas import PsychologySkillSpec


FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$", re.MULTILINE)


def load_skill_specs_from_directory(
    skills_dir: str | Path,
    *,
    include_duplicate_frontmatter_names: bool = False,
) -> list[PsychologySkillSpec]:
    """Build PsychologySkillSpec objects from .trae/skills/*/SKILL.md.

    The folder name is treated as the stable skill_id. This avoids collisions
    when a SKILL.md frontmatter name is duplicated or stale.
    """

    root = Path(skills_dir).expanduser()
    if not root.exists():
        raise FileNotFoundError(f"Skills directory does not exist: {root}")

    skill_files = sorted(root.glob("*/SKILL.md"))
    selected_files = skill_files
    if not include_duplicate_frontmatter_names:
        grouped: dict[str, list[Path]] = {}
        for skill_file in skill_files:
            markdown = skill_file.read_text(encoding="utf-8")
            frontmatter, _body = _split_frontmatter(markdown)
            frontmatter_name = frontmatter.get("name", skill_file.parent.name)
            grouped.setdefault(frontmatter_name, []).append(skill_file)

        selected_files = []
        for frontmatter_name, files in grouped.items():
            preferred = next((path for path in files if path.parent.name == frontmatter_name), None)
            selected_files.append(preferred or files[0])
        selected_files.sort()

    specs: list[PsychologySkillSpec] = []
    for skill_file in selected_files:
        markdown = skill_file.read_text(encoding="utf-8")
        frontmatter, body = _split_frontmatter(markdown)
        specs.append(_build_spec_from_markdown(skill_file.parent.name, skill_file, frontmatter, body, markdown))

    if not specs:
        raise FileNotFoundError(f"No SKILL.md files found under {root}")
    return specs


def _build_spec_from_markdown(
    skill_id: str,
    skill_file: Path,
    frontmatter: dict[str, str],
    body: str,
    markdown: str,
) -> PsychologySkillSpec:
    display_name = _extract_h1(body) or _title_from_id(skill_id)
    description = frontmatter.get("description") or _first_nonempty_line(_section(body, "Purpose"))

    use_when_section = _section_any(body, ["Use When", "Use-When Rules", "Use When Rules"])
    core_section = (
        _section(body, "Core Concepts")
        or _section(body, "Core Constructs")
        or _section(body, "Core Concept")
    )
    reasoning_principle = _section(body, "Reasoning Principle") or _section(body, "Mapping Principle")
    output_guidance = _section_any(body, ["Output Guidance", "Output Format"])
    reasoning_steps = _section(body, "Reasoning Steps")
    purpose = _section(body, "Purpose")
    routing_card_section = _section(body, "Routing Card")

    selection_hints = _bullets(use_when_section) or _ordered_items(use_when_section)
    if not selection_hints and description:
        selection_hints = [description]

    image_signals = _bullets(core_section)
    if not image_signals:
        image_signals = _keywords_from_text(" ".join([description, use_when_section]))

    analysis_steps = _ordered_items(reasoning_steps) or _bullets(reasoning_steps)
    if not analysis_steps:
        analysis_steps = _bullets(output_guidance)

    va_focus = _squash(reasoning_principle) or _squash(purpose) or description
    use_when = _squash(use_when_section) or description
    routing_card = _parse_routing_card(routing_card_section)
    if not routing_card:
        routing_card = _fallback_routing_card(selection_hints, image_signals, use_when, analysis_steps)

    return PsychologySkillSpec(
        skill_id=skill_id,
        display_name=display_name,
        short_description=description,
        theory_family=frontmatter.get("name", skill_id),
        selection_hints=selection_hints,
        use_when=use_when,
        image_signals=image_signals,
        va_focus=va_focus,
        analysis_steps=analysis_steps,
        routing_card=routing_card,
        source_path=str(skill_file),
        raw_skill_markdown=markdown,
    )


def _split_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(markdown)
    if not match:
        return {}, markdown

    raw_frontmatter = match.group("body")
    frontmatter: dict[str, str] = {}
    for line in raw_frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, markdown[match.end() :]


def _extract_h1(markdown: str) -> str:
    for match in HEADING_RE.finditer(markdown):
        if len(match.group("level")) == 1:
            return match.group("title").strip()
    return ""


def _section(markdown: str, title: str) -> str:
    headings = list(HEADING_RE.finditer(markdown))
    wanted = title.strip().lower()
    for index, match in enumerate(headings):
        current_title = match.group("title").strip().lower()
        if current_title != wanted:
            continue
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(markdown)
        return markdown[start:end].strip()
    return ""


def _section_any(markdown: str, titles: list[str]) -> str:
    for title in titles:
        section = _section(markdown, title)
        if section:
            return section
    return ""


def _bullets(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            items.append(stripped[2:].strip())
    return items


def _ordered_items(text: str) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*\d+\.\s+(?P<item>.+?)\s*$", line)
        if match:
            items.append(match.group("item").strip())
    return items


def _parse_routing_card(text: str) -> dict[str, list[str]]:
    label_map = {
        "USE WHEN": "use_when",
        "DO NOT USE WHEN": "do_not_use_when",
        "DO-NOT-USE-WHEN": "do_not_use_when",
        "VISUAL TRIGGERS": "visual_triggers",
        "NEAR-MISS BOUNDARIES": "near_miss_boundaries",
        "ROUTING PRIORITY": "routing_priority",
    }
    card: dict[str, list[str]] = {}
    current_key = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        label = stripped.rstrip(":").upper()
        if label in label_map:
            current_key = label_map[label]
            card.setdefault(current_key, [])
            continue

        if not current_key:
            continue

        if stripped.startswith(("- ", "* ")):
            item = stripped[2:].strip()
        else:
            item = stripped
        if item:
            card.setdefault(current_key, []).append(item)

    return {key: values for key, values in card.items() if values}


def _fallback_routing_card(
    selection_hints: list[str],
    image_signals: list[str],
    use_when: str,
    analysis_steps: list[str],
) -> dict[str, list[str]]:
    use_when_items = selection_hints[:3] or ([use_when] if use_when else [])
    card = {
        "use_when": use_when_items[:3],
        "visual_triggers": image_signals[:6],
        "routing_priority": analysis_steps[:2],
    }
    return {key: values for key, values in card.items() if values}


def _keywords_from_text(text: str) -> list[str]:
    candidates = [
        "face",
        "portrait",
        "nature",
        "landscape",
        "art",
        "design",
        "aesthetic",
        "complexity",
        "novelty",
        "social",
        "context",
        "emotion",
        "VA",
    ]
    lowered = text.lower()
    return [item for item in candidates if item.lower() in lowered]


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _squash(text: str) -> str:
    return " ".join(line.strip() for line in text.splitlines() if line.strip())


def _title_from_id(skill_id: str) -> str:
    return " ".join(part.capitalize() for part in skill_id.replace("_", "-").split("-"))
