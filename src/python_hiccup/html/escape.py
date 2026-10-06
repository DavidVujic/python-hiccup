"""Escape content for HTML."""

import html


def escape_content(data: str) -> str:
    """HTML content escaping wrapper."""
    return html.escape(data)


def escape_attribute(data: str) -> str:
    """HTML attribute escaping wrapper."""
    return escape_content(data)
