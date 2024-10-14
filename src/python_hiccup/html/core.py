"""Render HTML from a sequence of grouped data."""

import html
import operator
from collections.abc import Mapping, Sequence
from functools import reduce

from python_hiccup.transform import transform


def _element_allows_raw_content(element: str) -> bool:
    return str.lower(element) in {"script", "style"}


def _is_allowed_raw(content: str) -> bool:
    return str.startswith(content, "<!--") and str.endswith(content, "-->")


def _allow_raw_content(content: str, element: str) -> bool:
    if _element_allows_raw_content(element):
        return True

    return _is_allowed_raw(content)


def _escape(content: str, element: str) -> str:
    return content if _allow_raw_content(content, element) else html.escape(content)


def _join(acc: str, attrs: Sequence) -> str:
    return " ".join([acc, *attrs])


def _to_attributes(acc: str, attributes: Mapping) -> str:
    attrs = [f'{k}="{v}"' for k, v in attributes.items()]

    return _join(acc, attrs)


def _to_bool_attributes(acc: str, attributes: set) -> str:
    attrs = list(attributes)

    return _join(acc, attrs)


def _suffix(element_data: str) -> str:
    specials = {"doctype"}
    normalized = str.lower(element_data)

    return "" if any(s in normalized for s in specials) else " /"


def _to_html(tag: Mapping) -> list:
    element = next(iter(tag.keys()))
    child = next(iter(tag.values()))

    attributes = reduce(_to_attributes, tag.get("attributes", []), "")
    bool_attributes = reduce(_to_bool_attributes, tag.get("boolean_attributes", []), "")
    element_attributes = attributes + bool_attributes

    content = [_escape(str(c), element) for c in tag.get("content", [])]

    matrix = [_to_html(c) for c in child]
    flattened: list = reduce(operator.iadd, matrix, [])

    begin = f"{element}{element_attributes}" if element_attributes else element

    if flattened or content:
        return [f"<{begin}>", *flattened, *content, f"</{element}>"]

    extra = _suffix(begin)

    return [f"<{begin}{extra}>"]


def render(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    transformed = transform(data)

    matrix = [_to_html(t) for t in transformed]

    transformed_html: list = reduce(operator.iadd, matrix, [])

    return "".join(transformed_html)
