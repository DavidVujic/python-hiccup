from collections import defaultdict
from collections.abc import Mapping, Sequence
from functools import reduce


def _is_attribute(item: str | Mapping | Sequence) -> bool:
    return isinstance(item, dict)


def _is_child(item: str | Mapping | Sequence) -> bool:
    return isinstance(item, list | tuple)


def _is_content(item: str | Mapping | Sequence) -> bool:
    return not _is_attribute(item) and not _is_child(item)


def _key_for_group(item: str | Mapping | Sequence) -> str:
    if _is_attribute(item):
        return "attributes"
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


def transform(tags: Sequence) -> dict:
    first, *rest = tags

    element, extracted = _extract_from_tag(first)
    extra = [extracted, *rest]

    grouped: dict = reduce(_to_groups, extra, defaultdict(list))
    key = "children"

    children = grouped[key]

    branch = {element: [transform(r) for r in children]}
    options = {k: v for k, v in grouped.items() if k != key and v}

    return branch | options
