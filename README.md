# Python Hiccup

_Current status: experimental_

A Python implementation of the Hiccup syntax.
Python Hiccup is a library for representing HTML in Python.


Use `list` or `tuple` to represent HTML elements, and `dict` to represent the attributes of an element.


## Usage
Starting out as a fun challenge, and evolving into something that could be useful.

Creating server side HTML data using plain Python data structures, as an alternative to HTML server side templating (such as Jinja).
This library should also be possible to combine with PyScript, but I haven't tested that out yet.

## Example

Python:
``` python
from python_hiccup.html import render

render(["div", "Hello world!"])
```

The output will be a string: `<div>Hello world!</div>`


## Syntax

Python:
``` python
["div", "Hello world!"]
```

The HTML equivalent is:
``` html
<div>Hello world!</div>
```

Writing a nested HTML structure, using Python Hiccup:

``` python
["div", ["span", ["strong", "Hello world!"]]]
```

The HTML equivalent is:
``` html
<div>
    <span>
        <strong>Hello world!</strong>
    </span>
</div>
```


Adding attributes to an element, such as CSS id and classes, using Python Hiccup:

``` python
["div", {"id": "foo", "class": "bar"}, "Hello world!"]
```

or, using a more concise syntax:
``` python
["div#foo.bar", "Hello world!"]
```

The HTML equivalent is:
``` html
<div id="foo" class="bar">Hello world!</div>
```


## Resources
- [Hiccup](https://github.com/weavejester/hiccup) - the original implementation, for Clojure.


## Python alternatives
- [pyhiccup](https://github.com/nbessi/pyhiccup)
- [piccup](https://github.com/alexjuda/piccup)
