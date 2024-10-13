from python_hiccup.render import render_html
from python_hiccup.transform import transform


def todo_list(data: list[str]) -> list:
    return ["ul", {"class": "one"}, [["li", d] for d in data]]


def test_render_html_returns_a_string() -> None:
    data = ["div", "HELLO"]

    assert render_html(data) == "<div>HELLO</div>"


x = [
    "div#hello.first.second",
    "Hello & world",
    ["span", ["a#hello-world.highlight", {"href": "hello", "target": "_blank"}, "click here"]],
    ["span", ["span", ["strong", "HELLO"], ["strong", "WORLD"]]],
    [
        "figure",
        ["img", {"src": "picture.png"}],
        ["figcaption", "A description of the picture"],
    ],
    ["br"],
    todo_list(["one", "two", "three"]),
]

y = (
    "div#hello",
    ("span", ("a", "hello"), ("span", {"data-val-something": "this is some data"})),
)

z = [
    "script",
    """
const x = {one: 1};

if(x.one > 2) {
  console.log('hello world');
}
""",
]

siblings = [
    ["!DOCTYPE", {"html"}],
    ["html", ["head", ["title", "the web page"]], ["body", ["div", "HELLO WORLD"]]],
]
