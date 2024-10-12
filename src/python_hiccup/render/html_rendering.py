"""Render HTML from a sequence of grouped data.

The data is expected to be grouped into elements, attributes and content
"""

import html
import operator
from collections.abc import Mapping, Sequence
from functools import reduce

from python_hiccup.transform import transform


def _is_script_tag(element: str) -> bool:
    return str.lower(element) == "script"


def _escape(content: str, element: str) -> str:
    return content if _is_script_tag(element) else html.escape(content)


def _to_element_attributes(acc: str, attributes: Mapping) -> str:
    attrs = [f'{k}="{v}"' for k, v in attributes.items()]

    return " ".join([acc, *attrs])


def _to_html(tag: Mapping) -> list:
    element = next(iter(tag.keys()))
    child = next(iter(tag.values()))

    attributes = reduce(_to_element_attributes, tag.get("attributes", []), "")
    content = [_escape(c, element) for c in tag.get("content", [])]

    matrix = [_to_html(c) for c in child]
    flattened: list = reduce(operator.iadd, matrix, [])

    begin = f"{element}{attributes}" if attributes else element

    if flattened or content:
        return [f"<{begin}>", *flattened, *content, f"</{element}>"]

    return [f"<{begin} />"]


def render_html(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    transformed = transform(data)

    transformed_html = _to_html(transformed)

    return "".join(transformed_html)
