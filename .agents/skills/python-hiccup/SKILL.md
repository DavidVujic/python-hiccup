---
name: python-hiccup
description: Represent HTML and XML using plain Python data structures (lists, tuples, dicts) and render them to strings. Use when generating HTML/XML server-side or in PyScript with the python-hiccup library.
---

# Python Hiccup

Render HTML/XML from plain Python data structures: `["tag", "content"]` → `<tag>content</tag>`.

```python
from python_hiccup.html import render

render(["div", "Hello world!"])  # <div>Hello world!</div>
```

## Syntax

- Element: `["div", "Hello world!"]`
- Nested: `["div", ["span", ["strong", "Hello world!"]]]`
- A child can be a list of elements (rendered as siblings):

```python
render(["ul", [["li", i] for i in ["one", "two", "three"]]])
# <ul><li>one</li><li>two</li><li>three</li></ul>
```

## Attributes

Pass a `dict` right after the tag name; it maps attribute names to values:

```python
["div", {"id": "foo", "class": "bar"}, "Hello world!"]
# <div id="foo" class="bar">Hello world!</div>
```

Valueless attributes (e.g. `async`, `defer`) use a Python `set`:

```python
["!DOCTYPE", {"html"}]
["script", {"async"}, {"src": "js/script.js"}]
# <!DOCTYPE html><script async src="js/script.js"></script>
```

### Shorthand for id and classes

Instead of a `dict`, use `#` for the id and `.` for classes in the tag name:

```python
["div#foo.bar", "Hello world!"]
# <div id="foo" class="bar">Hello world!</div>
```

Multiple classes: `["div.bar.baz", ...]` → `<div class="bar baz">...</div>`

Unescaped content (e.g. HTML entities): `["div", raw("&copy;")]` (import `raw` from `python_hiccup.html`)

## XML

```python
from python_hiccup.xml import render

render(["Message", "Hello world!"])  # <Message>Hello world!</Message>
```

The XML declaration uses the special `?xml` tag:

```python
["?xml", {"version": 1.0}]
# <?xml version="1.0"?>
```

Include it as the first element of a document:

```python
document = [["?xml", {"version": 1.0}], ["actors", attributes, [john, eric]]]
```

XML namespaces go in the attributes dict:

```python
attributes = {"xmlns:fictional": "http://characters.example.com", "xmlns": "http://people.example.com"}
```
