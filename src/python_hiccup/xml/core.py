"""Render HTML from a sequence of grouped data."""

from collections.abc import Sequence
from xml.sax import saxutils

from python_hiccup.markup import render as render_markup


def escape(data: str) -> str:
    """XML content escaping wrapper."""
    return saxutils.escape(data)


def render(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    return render_markup(data, escape)
