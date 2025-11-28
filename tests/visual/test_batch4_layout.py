"""
Batch 4 Test: Layout & Containers
Tests: container, columns, column, grid, card, sidebar,
       tabs, tab, expander, accordion, modal, dialog, popover
"""
import umara as um

um.set_page_config(page_title="Batch 4: Layout & Containers", layout="wide")

um.title("Batch 4: Layout & Containers")
um.caption("Testing layout and container components")

um.divider()

# =============================================================================
# Basic Layout Components
# =============================================================================
um.header("Basic Layout Components", level=2)

um.subheader("container()")
with um.container():
    um.text("This is inside a container")
    um.info("Containers help organize content")

um.divider()

um.subheader("columns() and column()")
with um.columns(3):
    with um.column():
        with um.card():
            um.text("Column 1")
            um.metric("Metric A", "100")
    with um.column():
        with um.card():
            um.text("Column 2")
            um.metric("Metric B", "200")
    with um.column():
        with um.card():
            um.text("Column 3")
            um.metric("Metric C", "300")

um.divider()

um.subheader("columns() - Custom widths")
with um.columns([1, 2, 1]):
    with um.column():
        um.info("Narrow (1)")
    with um.column():
        um.success("Wide (2)")
    with um.column():
        um.warning("Narrow (1)")

um.divider()

# =============================================================================
# Grid Layout
# =============================================================================
um.header("Grid Layout", level=2)

um.subheader("grid()")
with um.grid(cols=4, gap="1rem"):
    for i in range(8):
        with um.card():
            um.text(f"Grid Item {i + 1}")
            um.caption("Card content")

um.divider()

# =============================================================================
# Card Component
# =============================================================================
um.header("Card Component", level=2)

with um.columns(3):
    with um.column():
        um.subheader("card() - Basic")
        with um.card():
            um.text("Basic Card")
            um.caption("With some content inside")

    with um.column():
        um.subheader("card() - With title")
        with um.card(title="Card Title"):
            um.text("Card content goes here")

    with um.column():
        um.subheader("card() - Styled")
        with um.card(title="Styled Card"):
            um.metric("Value", "42", delta="5")

um.divider()

# =============================================================================
# Tabs Component
# =============================================================================
um.header("Tabs Component", level=2)

um.subheader("tabs() and tab()")
with um.tabs(["Overview", "Details", "Settings"]):
    with um.tab("Overview"):
        um.text("This is the overview tab content")
        um.info("Welcome to the overview!")

    with um.tab("Details"):
        um.text("This is the details tab content")
        um.markdown("- Detail 1\n- Detail 2\n- Detail 3")

    with um.tab("Settings"):
        um.text("This is the settings tab content")
        um.checkbox("Enable feature", key="tab_checkbox")

um.divider()

# =============================================================================
# Expander & Accordion
# =============================================================================
um.header("Expander & Accordion", level=2)

with um.columns(2):
    with um.column():
        um.subheader("expander()")
        with um.expander("Click to expand"):
            um.text("This content is hidden by default")
            um.code("print('Hello from expander!')", language="python")

        with um.expander("Already expanded", expanded=True):
            um.text("This expander starts open")

    with um.column():
        um.subheader("accordion()")
        with um.accordion("FAQ"):
            with um.expander("What is Umara?"):
                um.text("Umara is a Python UI framework")
            with um.expander("How do I use it?"):
                um.text("Import umara and start building!")
            with um.expander("Is it free?"):
                um.text("Yes, it's open source!")

um.divider()

# =============================================================================
# Modal & Dialog
# =============================================================================
um.header("Modal & Dialog", level=2)

with um.columns(2):
    with um.column():
        um.subheader("modal()")
        if um.button("Open Modal", key="btn_modal"):
            um.open_modal("example_modal")

        with um.modal("example_modal", title="Example Modal"):
            um.text("This is modal content!")
            um.input("Enter something", key="modal_input")
            if um.button("Close", key="btn_close_modal"):
                um.close_modal("example_modal")

    with um.column():
        um.subheader("dialog()")
        if um.button("Open Dialog", key="btn_dialog"):
            um.open_modal("example_dialog")

        with um.dialog("example_dialog", title="Confirm Action"):
            um.text("Are you sure you want to proceed?")
            with um.columns(2):
                with um.column():
                    if um.button("Cancel", key="btn_cancel", variant="secondary"):
                        um.close_modal("example_dialog")
                with um.column():
                    if um.button("Confirm", key="btn_confirm"):
                        um.close_modal("example_dialog")
                        um.success("Action confirmed!")

um.divider()

# =============================================================================
# Popover & Tooltip
# =============================================================================
um.header("Popover & Tooltip", level=2)

with um.columns(2):
    with um.column():
        um.subheader("popover()")
        with um.popover("Click for info"):
            um.text("Popover content")
            um.caption("This shows on click")

    with um.column():
        um.subheader("tooltip()")
        um.tooltip("This is a tooltip", "Hover over me!")
        um.text(" ")
        um.tooltip("Additional info here", "More tooltips")

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `container()` | ✅ | Basic container |
| `columns()` | ✅ | Equal and custom widths |
| `column()` | ✅ | Inside columns |
| `grid()` | ✅ | Custom cols and gap |
| `card()` | ✅ | Basic and with title |
| `tabs()` | ✅ | Multiple tabs |
| `tab()` | ✅ | Tab content |
| `expander()` | ✅ | Collapsed and expanded |
| `accordion()` | ✅ | Multiple expanders |
| `modal()` | ✅ | Open/close functionality |
| `dialog()` | ✅ | Confirmation dialog |
| `popover()` | ✅ | Click-triggered |
| `tooltip()` | ✅ | Hover text |
""")

um.caption("Batch 4 test complete - verify all layout components work correctly")
