"""Unit tests for the python_hiccup.html.render function."""

from python_hiccup.html import render


def test_returns_a_string() -> None:
    """Assert that the render function returns a string containing HTML."""
    data = ["div", "HELLO"]

    assert render(data) == "<div>HELLO</div>"


def test_accepts_a_sequence_of_tuples() -> None:
    """Assert that the render function accepts tuples as input."""
    data = ("div", ("span", "HELLO"))

    assert render(data) == "<div><span>HELLO</span></div>"


def test_handles_special_tags() -> None:
    """Assert that the HTML render function takes any special elements into account when."""
    assert render(["!DOCTYPE"]) == "<!DOCTYPE>"
    assert render(["div"]) == "<div />"


def test_parses_attributes() -> None:
    """Assert that element attributes are parsed as expected."""
    data = ["div", {"id": "hello", "class": "first second"}, "HELLO WORLD"]

    expected = '<div id="hello" class="first second">HELLO WORLD</div>'

    assert render(data) == expected


def test_parses_attribute_shorthand() -> None:
    """Assert that the shorthand feature for element id and class is parsed as expected."""
    data = ["div#hello.first.second", "HELLO WORLD"]

    expected = '<div id="hello" class="first second">HELLO WORLD</div>'

    assert render(data) == expected


def test_parses_boolean_attributes() -> None:
    """Assert that attributes without values, such as async or defer, is parsed as expected."""
    data = ["script", {"async"}, {"src": "path/to/script"}]

    expected = '<script src="path/to/script" async />'

    assert render(data) == expected


def test_accepts_sibling_elements() -> None:
    """Assert that the render function accepts a structure of top-level siblings."""
    siblings = [
        ["!DOCTYPE", {"html"}],
        ["html", ["head", ["title", "hey"]], ["body", "HELLO WORLD"]],
    ]

    expected = "<!DOCTYPE html><html><head><title>hey</title></head><body>HELLO WORLD</body></html>"

    assert render(siblings) == expected


def test_escapes_content() -> None:
    """Assert that the render function will HTML escape the inner content of elements."""
    data = ["div", "Hello & <Goodbye>"]

    expected = "<div>Hello &amp; &lt;Goodbye&gt;</div>"

    assert render(data) == expected


def test_does_not_escape_script_content() -> None:
    """Assert that content within a script tag is not escaped.

    Making it possible to add inline JS.
    """
    script_content = "if(x.one > 2) {console.log('hello world');}"
    data = ["script", script_content]
    expected = f"<script>{script_content}</script>"

    assert render(data) == expected


def test_does_not_escape_comment_content() -> None:
    """Assert that content within an HTML comment tag is not escaped."""
    data = ["div", "<!--Hello & <Goodbye>-->"]
    expected = "<div><!--Hello & <Goodbye>--></div>"

    assert render(data) == expected


def test_does_not_escape_inline_style_tag_content() -> None:
    """Assert that content within a style tag is not escaped.

    Making it possible to construct inline CSS.
    """
    content = """
p {
  color: red;
}

div span.something {
  color: blue;
}

"""
    data = ["style", content]
    expected = f"<style>{content}</style>"

    assert render(data) == expected


def test_generates_an_element_with_children() -> None:
    """Assert that an element with children is rendered."""
    items = ["a", "b", "c"]

    data = ["ul", [["li", i] for i in items]]

    assert render(data) == "<ul><li>a</li><li>b</li><li>c</li></ul>"


def test_allows_numeric_values_in_content() -> None:
    """Assert that numeric values are allowed as the content of an element."""
    data = ["ul", ["li", 1]]

    assert render(data) == "<ul><li>1</li></ul>"
