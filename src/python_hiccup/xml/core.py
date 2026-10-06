"""Render HTML from a sequence of grouped data."""

from collections.abc import Sequence

from python_hiccup.markup import render as render_markup
from python_hiccup.xml import escape


def render(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    return render_markup(data, escape)
