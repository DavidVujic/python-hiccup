"""Render HTML from a sequence of grouped data."""

import html
import operator
from collections.abc import Mapping, Sequence
from functools import reduce
from itertools import filterfalse as reject

from python_hiccup.transform import CONTENT_TAG, HTML_SETTER, transform


def _has_setter(container: dict | list) -> bool:
    return operator.contains(container, HTML_SETTER)


def _has_content(container: dict | list) -> bool:
    return operator.contains(container, CONTENT_TAG)


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
    attrs = [f'{k}="{v}"' for k, v in attributes.items() if k != HTML_SETTER]

    return _join(acc, attrs)


def _to_bool_attributes(acc: str, attributes: set) -> str:
    attrs = list(attributes)

    return _join(acc, attrs)


def _closing_tag(element: str) -> bool:
    specials = {"script"}

    return str.lower(element) in specials


def _suffix(element_data: str) -> str:
    specials = {"doctype"}
    normalized = str.lower(element_data)

    return "" if any(s in normalized for s in specials) else " /"


def _is_content(element: str) -> bool:
    return element == CONTENT_TAG


def _to_html(tag: Mapping, parent: str = "", rename: str | None = None) -> list:
    element = next(iter(tag.keys()))
    child = next(iter(tag.values()))

    html_setter = next(filter(_has_setter, tag.get("attributes", [])), None)

    if html_setter is not None:
        return "".join(
            _to_html(
                {
                    "script": [
                        *reject(_has_content, tag[element]),
                        {CONTENT_TAG: html_setter[HTML_SETTER].get("__html", "")},
                    ],
                    "attributes": [
                        *reject(_has_setter, tag["attributes"]),
                        dict(reject(_has_setter, html_setter.items())),
                    ],
                },
                parent,
                rename=element,
            )
        )

    if _is_content(element):
        return [_escape(str(child), parent)]

    tag_name = rename or element

    attributes = reduce(_to_attributes, tag.get("attributes", []), "")
    bool_attributes = reduce(_to_bool_attributes, tag.get("boolean_attributes", []), "")
    element_attributes = attributes + bool_attributes

    matrix = [_to_html(c, element) for c in child]
    flattened: list = reduce(operator.iadd, matrix, [])

    begin = f"{tag_name}{element_attributes}" if element_attributes else tag_name

    if flattened:
        return [f"<{begin}>", *flattened, f"</{tag_name}>"]

    if _closing_tag(tag_name):
        return [f"<{begin}>", f"</{tag_name}>"]

    extra = _suffix(begin)

    return [f"<{begin}{extra}>"]


def render(data: Sequence) -> str:
    """Transform a sequence of grouped data to HTML."""
    transformed = transform(data)

    matrix = [_to_html(t) for t in transformed]

    transformed_html: list = reduce(operator.iadd, matrix, [])

    return "".join(transformed_html)
