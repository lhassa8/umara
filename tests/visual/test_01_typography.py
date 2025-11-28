"""Comprehensive test for Typography components"""
import umara as um

um.set_page_config(page_title="Typography Test", layout="wide")

um.title("Typography Components Test")

# text()
um.subheader("1. text()")
um.text("Regular text content")
um.text("Bold text", style={"fontWeight": "bold"})
um.text("Colored text", style={"color": "blue"})

um.divider()

# title()
um.subheader("2. title()")
um.title("This is a Title")

um.divider()

# header()
um.subheader("3. header()")
um.header("This is a Header")

um.divider()

# subheader()
um.subheader("4. subheader()")
um.subheader("This is a Subheader")

um.divider()

# caption()
um.subheader("5. caption()")
um.caption("This is a caption - smaller, muted text")

um.divider()

# markdown()
um.subheader("6. markdown()")
um.markdown("""
## Markdown Test

This is **bold** and *italic* and ~~strikethrough~~.

### List:
- Item 1
- Item 2
- Item 3

### Code:
```python
def hello():
    print("Hello World")
```

### Table:
| Name | Age | City |
|------|-----|------|
| John | 25 | NYC |
| Jane | 30 | LA |
""")

um.divider()

# code()
um.subheader("7. code()")
um.code("""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
""", language="python")

um.divider()

# latex()
um.subheader("8. latex()")
um.latex(r"E = mc^2")
um.latex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")

um.divider()

# echo()
um.subheader("9. echo()")
with um.echo():
    x = 5
    y = 10
    result = x + y
    um.text(f"Result: {result}")

um.divider()

# write()
um.subheader("10. write()")
um.write("Simple text via write()")
um.write({"key": "value", "number": 42, "list": [1, 2, 3]})
um.write([1, 2, 3, 4, 5])

um.divider()

um.success("Typography components test completed!")
