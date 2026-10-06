"""Escape content for XML."""

import re
from xml.sax import saxutils

_CDATA_BEGIN = "<![CDATA["
_CDATA_END = "]]>"

_CDATA_PATTERN = re.compile(rf"({re.escape(_CDATA_BEGIN)}.*?{re.escape(_CDATA_END)})", re.DOTALL)


def escape_content_with_cdata(data: str) -> str:
    """XML escaping for content with CDATA sections.

    Content is escaped, except CDATA sections that are left unescaped.
    This is according to the XML specification.

    """
    parts = _CDATA_PATTERN.split(data)
    escaped = [p if i % 2 else saxutils.escape(p) for i, p in enumerate(parts)]

    return "".join(escaped)


def escape_content(data: str) -> str:
    """XML content escaping wrapper."""
    return escape_content_with_cdata(data) if _CDATA_BEGIN in data else saxutils.escape(data)


def escape_attribute(data: str) -> str:
    """XML attribute escaping wrapper."""
    return saxutils.escape(data)
