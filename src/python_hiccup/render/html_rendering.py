import html
import operator
from collections.abc import Mapping, Sequence
from functools import reduce

from python_hiccup.transform import transform


def is_script_tag(element: str) -> bool:
    return str.lower(element) == "script"


def escape(content: str, element: str) -> str:
    return content if is_script_tag(element) else html.escape(content)


def to_element_attributes(acc: str, attributes: Mapping) -> str:
    attrs = [f'{k}="{v}"' for k, v in attributes.items()]

    return " ".join([acc, *attrs])


def to_html(tag: Mapping) -> list:
    element = next(iter(tag.keys()))
    child = next(iter(tag.values()))

    attributes = reduce(to_element_attributes, tag.get("attributes", []), "")
    content = [escape(c, element) for c in tag.get("content", [])]

    matrix = [to_html(c) for c in child]
    flattened: list = reduce(operator.iadd, matrix, [])

    begin = f"{element}{attributes}" if attributes else element

    if flattened or content:
        return [f"<{begin}>", *flattened, *content, f"</{element}>"]

    return [f"<{begin} />"]


def render_html(data: Sequence) -> str:
    transformed = transform(data)

    transformed_html = to_html(transformed)

    return "".join(transformed_html)
