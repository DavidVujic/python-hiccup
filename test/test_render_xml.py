"""Unit tests for the python_hiccup.xml.render function."""

from python_hiccup.xml import render


def test_returns_a_string() -> None:
    """Assert that the render function returns a string containing HTML."""
    data = ["Message", "HELLO"]

    assert render(data) == "<Message>HELLO</Message>"


def test_handles_special_tags() -> None:
    """Assert that the render function takes any special elements into account."""
    assert render(["!DOCTYPE"]) == "<!DOCTYPE>"

    assert render(["?xml"]) == "<?xml?>"

    assert render(["HelloWorld"]) == "<HelloWorld />"


def test_parses_attributes() -> None:
    """Assert that element attributes are parsed as expected."""
    data = ["?xml", {"version": "1.0", "encoding": "UTF-8"}]

    expected = '<?xml version="1.0" encoding="UTF-8"?>'

    assert render(data) == expected


def test_escapes_content() -> None:
    """Assert that the render function will escape the inner content of elements."""
    data = ["Message", "Hello > Bye & 0 < 1"]

    expected = "<Message>Hello &gt; Bye &amp; 0 &lt; 1</Message>"

    assert render(data) == expected


def test_escapes_content_but_not_CDATA() -> None:
    """Assert that the render function escapes inner content, but not the data in CDATA sections."""
    data = ["Message", "Hello > Bye & 0 < 1 <![CDATA[ < DATA > & ]]>"]

    expected = "<Message>Hello &gt; Bye &amp; 0 &lt; 1 <![CDATA[ < DATA > & ]]></Message>"

    assert render(data) == expected


def test_escapes_content_in_attributes() -> None:
    """Assert that the render function will escape the content of attributes."""
    data = ["Message", {"value": "Hello & <Goodbye>"}]

    expected = '<Message value="Hello &amp; &lt;Goodbye&gt;" />'

    assert render(data) == expected


def test_generates_an_element_with_children() -> None:
    """Assert that an element with children is rendered."""
    data = ["data", ["item", "Python"]]

    assert render(data) == "<data><item>Python</item></data>"


def test_generates_an_namespaced_element_with_children() -> None:
    """Assert that an element with children is rendered."""
    data = [["name", "John Cleese"], ["fictional:character", "Archie Leach"]]

    expected = "<name>John Cleese</name><fictional:character>Archie Leach</fictional:character>"
    assert render(data) == expected
