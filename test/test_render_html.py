from python_hiccup.html import render


def todo_list(data: list[str]) -> list:
    return ["ul", {"class": "one"}, [["li", d] for d in data]]


def test_returns_a_string() -> None:
    data = ["div", "HELLO"]

    assert render(data) == "<div>HELLO</div>"


def test_accepts_a_sequence_of_tuples() -> None:
    data = ("div", ("span", "HELLO"))

    assert render(data) == "<div><span>HELLO</span></div>"


def test_handles_special_tags() -> None:
    assert render(["!DOCTYPE"]) == "<!DOCTYPE>"
    assert render(["div"]) == "<div />"


def test_parses_attributes() -> None:
    data = ["div", {"id": "hello", "class": "first second"}, "HELLO WORLD"]

    expected = '<div id="hello" class="first second">HELLO WORLD</div>'

    assert render(data) == expected


def test_parses_attribute_shorthand() -> None:
    data = ["div#hello.first.second", "HELLO WORLD"]

    expected = '<div id="hello" class="first second">HELLO WORLD</div>'

    assert render(data) == expected


def test_parses_boolean_attributes() -> None:
    data = ["script", {"async"}, {"src": "path/to/script"}]

    expected = '<script src="path/to/script" async />'

    assert render(data) == expected


def test_accepts_sibling_elements() -> None:
    siblings = [
        ["!DOCTYPE", {"html"}],
        ["html", ["head", ["title", "hey"]], ["body", "HELLO WORLD"]],
    ]

    expected = "<!DOCTYPE html><html><head><title>hey</title></head><body>HELLO WORLD</body></html>"

    assert render(siblings) == expected


def test_escapes_content() -> None:
    data = ["div", "Hello & <Goodbye>"]

    expected = "<div>Hello &amp; &lt;Goodbye&gt;</div>"

    assert render(data) == expected


def test_does_not_escape_script_content() -> None:
    script_content = "if(x.one > 2) {console.log('hello world');}"
    data = ["script", script_content]
    expected = f"<script>{script_content}</script>"

    assert render(data) == expected
