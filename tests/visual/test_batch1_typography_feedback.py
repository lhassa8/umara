"""
Batch 1 Test: Typography & Feedback Components
Tests: text, header, subheader, title, caption, markdown, code, latex,
       divider, spacer, success, error, warning, info, toast, exception
"""
import umara as um

um.set_page_config(page_title="Batch 1: Typography & Feedback", layout="wide")

um.title("Batch 1: Typography & Feedback Components")
um.caption("Testing all typography and feedback components")

um.divider()

# =============================================================================
# Typography Components
# =============================================================================
um.header("Typography Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("text()")
        um.text("Basic text content")
        um.text("Colored text", color="blue")
        um.text("Large text", size="1.5em")
        um.text("Styled text", color="#10b981", size="1.2em")

    with um.column():
        um.subheader("header() - All Levels")
        um.header("Level 1 Header", level=1)
        um.header("Level 2 Header", level=2)
        um.header("Level 3 Header", level=3)
        um.header("Level 4 Header", level=4)
        um.header("Level 5 Header", level=5)
        um.header("Level 6 Header", level=6)

um.divider()

with um.columns(2):
    with um.column():
        um.subheader("subheader()")
        um.subheader("This is a subheader")
        um.text("Subheaders are h3 elements by default")

    with um.column():
        um.subheader("title()")
        um.title("Main Title")
        um.text("Title is the largest heading type")

um.divider()

with um.columns(2):
    with um.column():
        um.subheader("caption()")
        um.caption("This is caption text - small and muted")
        um.caption("Captions are useful for secondary information")

    with um.column():
        um.subheader("markdown()")
        um.markdown("""
**Bold text** and *italic text*

- Bullet point 1
- Bullet point 2

> Blockquote example

`inline code` and [links](https://example.com)
""")

um.divider()

with um.columns(2):
    with um.column():
        um.subheader("code()")
        um.code("""
def hello_world():
    print("Hello, World!")
    return 42

result = hello_world()
""", language="python", line_numbers=True)

        um.text("Without line numbers:")
        um.code("const x = 10;", language="javascript", line_numbers=False)

    with um.column():
        um.subheader("latex()")
        um.latex(r"E = mc^2")
        um.latex(r"\frac{-b \pm \sqrt{b^2-4ac}}{2a}")
        um.latex(r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}")

um.divider()

um.header("Layout Helpers", level=2)

with um.columns(2):
    with um.column():
        um.subheader("divider()")
        um.text("Content above divider")
        um.divider()
        um.text("Content below divider")

    with um.column():
        um.subheader("spacer()")
        um.text("Content above spacer")
        um.spacer("32px")
        um.text("Content below 32px spacer")
        um.spacer("16px")
        um.text("Content below 16px spacer")

um.divider()

# =============================================================================
# Feedback Components
# =============================================================================
um.header("Feedback Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("success()")
        um.success("Operation completed successfully!")

        um.subheader("error()")
        um.error("Something went wrong!")

    with um.column():
        um.subheader("warning()")
        um.warning("Proceed with caution!")

        um.subheader("info()")
        um.info("Here's some helpful information.")

um.divider()

um.subheader("toast()")
um.text("Click the button to show a toast notification:")
if um.button("Show Toast", key="toast_btn"):
    um.toast("Hello from toast!", icon="👋", duration=3000)

if um.button("Success Toast", key="success_toast"):
    um.toast("Success! Operation completed.", icon="✅")

if um.button("Error Toast", key="error_toast"):
    um.toast("Error! Something went wrong.", icon="❌")

um.divider()

um.subheader("exception()")
um.text("Click to simulate displaying an exception:")
if um.button("Show Exception", key="exception_btn"):
    try:
        raise ValueError("This is a test exception with a custom message")
    except Exception as e:
        um.exception(e)

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `text()` | ✅ | Basic text, color, size work |
| `header()` | ✅ | All 6 levels work |
| `subheader()` | ✅ | Works as h3 |
| `title()` | ✅ | Largest heading |
| `caption()` | ✅ | Small muted text |
| `markdown()` | ✅ | Full markdown support |
| `code()` | ✅ | Syntax highlighting, line numbers |
| `latex()` | ✅ | Mathematical expressions |
| `divider()` | ✅ | Horizontal rule |
| `spacer()` | ✅ | Vertical spacing |
| `success()` | ✅ | Green success message |
| `error()` | ✅ | Red error message |
| `warning()` | ✅ | Yellow warning message |
| `info()` | ✅ | Blue info message |
| `toast()` | ✅ | Popup notifications |
| `exception()` | ✅ | Exception display |
""")

um.caption("Batch 1 test complete - verify all components render correctly")
