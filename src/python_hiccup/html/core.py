"""Render HTML from a sequence of grouped data."""

from collections.abc import Sequence

from python_hiccup.html import escape
from python_hiccup.markup import render as render_markup


def render(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    return render_markup(data, escape)
