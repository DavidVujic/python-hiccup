"""Transform a sequence of tag data into groups."""

from collections import defaultdict
from collections.abc import Mapping, Sequence
from functools import reduce

Item = str | set | Mapping | Sequence


def _is_attribute(item: Item) -> bool:
    return isinstance(item, dict)


def _is_boolean_attribute(item: Item) -> bool:
    return isinstance(item, set)


def _is_child(item: Item) -> bool:
    return isinstance(item, list | tuple)


def _is_content(item: Item) -> bool:
    pipeline = [_is_attribute, _is_boolean_attribute, _is_child]

    return not any(fn(item) for fn in pipeline)


def _is_sibling(item: str | Mapping | Sequence) -> bool:
    return _is_child(item)


def _key_for_group(item: str | Mapping | Sequence) -> str:
    if _is_attribute(item):
        return "attributes"
    if _is_boolean_attribute(item):
        return "boolean_attributes"
    if _is_content(item):
        return "content"

    return "children"


def _to_groups(acc: dict, item: str | Mapping | Sequence) -> dict:
    key = _key_for_group(item)

    flattened = item[0] if _is_child(item) and _is_child(item[0]) else item
    value = acc[key] + [flattened]

    return acc | {key: value}


def _extract_from_tag(tag: str) -> tuple[str, dict]:
    first, *rest = tag.split(".")
    element_name, _id = first.split("#") if "#" in first else (first, "")

    element_id = {"id": _id} if _id else {}
    element_class = {"class": " ".join(rest)} if rest else {}

    return element_name, element_id | element_class


def _transform_tags(tags: Sequence) -> dict:
    first, *rest = tags

    element, extracted = _extract_from_tag(first)
    extra = [extracted, *rest]

    grouped: dict = reduce(_to_groups, extra, defaultdict(list))
    key = "children"

    children = grouped[key]

    branch = {element: [_transform_tags(r) for r in children]}
    options = {k: v for k, v in grouped.items() if k != key and v}

    return branch | options


def transform(tags: Sequence) -> list:
    """Transform a sequence of tag data into goups: elements, attributes and content."""
    first, *rest = tags

    if _is_sibling(first):
        return [_transform_tags(t) for t in tags]

    return [_transform_tags(tags)]
