"""Transform a sequence of tag data into groups."""

from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from collections.abc import Set as AbstractSet
from functools import reduce

Item = str | AbstractSet | Mapping | Sequence | Callable

ATTRIBUTES = "attributes"
BOOLEAN_ATTRIBUTES = "boolean_attributes"
CHILDREN = "children"

CONTENT_TAG = "<::HICCUP_CONTENT::>"


def _is_attribute(item: Item) -> bool:
    return isinstance(item, dict)


def _is_boolean_attribute(item: Item) -> bool:
    return isinstance(item, set)


def _is_child(item: Item) -> bool:
    return isinstance(item, list | tuple)


def _is_sibling(item: Item) -> bool:
    return _is_child(item)


def _key_for_group(item: Item) -> str:
    if _is_attribute(item):
        return ATTRIBUTES
    if _is_boolean_attribute(item):
        return BOOLEAN_ATTRIBUTES

    return CHILDREN


def _to_groups(acc: dict, item: Item) -> dict:
    key = _key_for_group(item)

    flattened = [*item] if isinstance(item, Sequence) and _is_child(item[0]) else [item]

    value = acc[key] + flattened

    return acc | {key: value}


def _extract_from_tag(tag: str) -> tuple[str, dict]:
    first, *rest = tag.split(".")
    element_name, _id = first.split("#") if "#" in first else (first, "")

    element_id = {"id": _id} if _id else {}
    element_class = {"class": " ".join(rest)} if rest else {}

    return element_name, element_id | element_class


def _transform_tags(tags: Sequence) -> dict:
    if not isinstance(tags, list | tuple):
        return {CONTENT_TAG: tags}

    first, *rest = tags

    element, extracted = _extract_from_tag(first)
    extra = [extracted, *rest]

    grouped: dict = reduce(_to_groups, extra, defaultdict(list))
    children = grouped[CHILDREN]

    branch = {element: [_transform_tags(r) for r in children]}
    options = {k: v for k, v in grouped.items() if k != CHILDREN and v}

    return branch | options


def transform(tags: Sequence) -> list:
    """Transform a sequence of tag data into goups: elements, attributes and content."""
    first, *_ = tags

    if _is_sibling(first):
        return [_transform_tags(t) for t in tags]

    return [_transform_tags(tags)]
