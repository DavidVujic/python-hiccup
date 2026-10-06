"""Escape content for XML."""

from xml.sax import saxutils


def escape_content(data: str) -> str:
    """XML content escaping wrapper."""
    return saxutils.escape(data)


def escape_attribute(data: str) -> str:
    """XML attribute escaping wrapper."""
    return escape_content(data)
