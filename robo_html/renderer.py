"""Render a self-contained HTML report from a template and canonical JSON data."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Mapping


class HtmlReportGenerator:
    """Render report data into a caller-supplied standalone HTML template.

    The application owns its branding/template and canonical report data model.
    ``robo-html`` owns only the generic rendering and safe JSON embedding.
    """

    DEFAULT_DATA_PLACEHOLDER = "__ROBO_REPORT_DATA_JSON__"

    @classmethod
    def _load_template(cls, template_path: Path, data_placeholder: str) -> str:
        template = Path(template_path).read_text(encoding="utf-8")
        if data_placeholder not in template:
            raise ValueError(
                f"HTML report template {template_path} does not contain "
                f"the required placeholder {data_placeholder!r}."
            )
        return template

    @staticmethod
    def _prepare_data(data: Mapping[str, Any]) -> dict[str, Any]:
        """Return an isolated JSON-ready copy without application mutation."""
        prepared = copy.deepcopy(dict(data))
        if not isinstance(prepared.get("results", []), list):
            prepared["results"] = []
        return prepared

    @staticmethod
    def _serialize_for_html(data: Mapping[str, Any]) -> str:
        """Serialize JSON safely for an ``application/json`` script element."""
        payload = json.dumps(data, ensure_ascii=False, default=str)
        return (
            payload.replace("&", "\\u0026")
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029")
        )

    @classmethod
    def generate(
        cls,
        data: Mapping[str, Any],
        *,
        template_path: Path,
        data_placeholder: str = DEFAULT_DATA_PLACEHOLDER,
    ) -> str:
        """Render one self-contained HTML document from canonical report data."""
        prepared = cls._prepare_data(data)
        template = cls._load_template(Path(template_path), data_placeholder)
        return template.replace(
            data_placeholder,
            cls._serialize_for_html(prepared),
            1,
        )

    @classmethod
    def generate_from_json(
        cls,
        json_path: Path,
        *,
        template_path: Path,
        data_placeholder: str = DEFAULT_DATA_PLACEHOLDER,
    ) -> str:
        """Render HTML from a persisted canonical JSON report."""
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"Report JSON must contain an object: {json_path}")
        return cls.generate(
            data,
            template_path=template_path,
            data_placeholder=data_placeholder,
        )
