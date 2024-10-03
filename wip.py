from collections import defaultdict
from functools import reduce
from typing import Any


def todo_list(data: list[str]) -> list:
    return ["ul", {"class": "one"}, [["li", d] for d in data]]


def is_attribute(item: Any) -> bool:
    return isinstance(item, dict)


def is_child(item: Any) -> bool:
    return isinstance(item, list | tuple)


def is_content(item: Any) -> bool:
    return not is_attribute(item) and not is_child(item)


def key_for_group(item: Any) -> str:
    if is_attribute(item):
        return "attributes"
    if is_content(item):
        return "content"

    return "children"


def to_groups(acc: dict, item: Any) -> dict:
    key = key_for_group(item)

    flattened = item[0] if is_child(item) and is_child(item[0]) else item
    value = acc[key] + [flattened]

    return acc | {key: value}


def transform(tag: list) -> dict:
    first, *rest = tag

    grouped: dict = reduce(to_groups, rest, defaultdict(list))
    key = "children"

    children = grouped[key]

    branch = {first: [transform(r) for r in children]}
    options = {k: v for k, v in grouped.items() if k != key and v}

    return branch | options


def transform_attribute(acc: str, attributes: dict) -> str:
    attrs = [f'{k}="{v}"' for k, v in attributes.items()]
    joined = " ".join(attrs)

    return acc + joined


def transform_html(tag: dict) -> list:
    node = next(iter(tag.keys()))
    child = next(iter(tag.values()))

    attributes = reduce(transform_attribute, tag.get("attributes", []), "")
    content = tag.get("content", [])

    matrix = [transform_html(c) for c in child]
    flattened = sum(matrix, [])

    begin = f"{node} {attributes}" if attributes else node

    if flattened or content:
        return [f"<{begin}>"] + flattened + content + [f"</{node}>"]

    return [f"<{begin} />"]


def render(data: list):
    transformed = transform(data)

    transformed_html = transform_html(transformed)

    return "".join(transformed_html)


z = [
    "div",
    {"class": "first second"},
    ["span", ["a", {"href": "hello", "target": "_blank"}]],
    ["span", ["span", ["strong", "HELLO"], ["strong", "WORLD"]]],
    [
        "figure",
        ["img", {"src": "picture.png"}],
        ["figcaption", "A description of the picture"],
    ],
    ["br"],
    todo_list(["one", "two", "three"]),
]

y = ("div", ("span", ("a", "hello")))
