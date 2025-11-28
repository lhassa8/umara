"""Comprehensive test for Container components"""
import umara as um

um.set_page_config(page_title="Containers Test", layout="wide")

um.title("Container Components Test")

# expander()
um.subheader("1. expander()")
with um.expander("Click to expand", expanded=False):
    um.text("This is hidden content inside the expander")
    um.info("You expanded me!")

um.divider()

# accordion()
um.subheader("2. accordion()")
with um.accordion("Accordion Item 1", key="acc1"):
    um.text("Content of accordion item 1")
with um.accordion("Accordion Item 2", key="acc2"):
    um.text("Content of accordion item 2")
with um.accordion("Accordion Item 3", key="acc3"):
    um.text("Content of accordion item 3")

um.divider()

# modal()
um.subheader("3. modal()")
if um.button("Open Modal", key="open_modal_btn"):
    um.open_modal("sample_modal")

with um.modal("sample_modal", title="Sample Modal"):
    um.text("This is modal content!")
    um.info("Modal dialogs are useful for confirmations")
    if um.button("Close Modal", key="close_modal_btn"):
        um.close_modal("sample_modal")

um.divider()

# dialog()
um.subheader("4. dialog()")
if um.button("Open Dialog", key="open_dialog_btn"):
    um.open_modal("sample_dialog")

with um.dialog("sample_dialog", title="Confirm Action"):
    um.text("Are you sure you want to proceed?")
    with um.columns(2):
        with um.column():
            if um.button("Cancel", key="dialog_cancel"):
                um.close_modal("sample_dialog")
        with um.column():
            if um.button("Confirm", key="dialog_confirm"):
                um.success("Action confirmed!")
                um.close_modal("sample_dialog")

um.divider()

# popover()
um.subheader("5. popover()")
with um.popover("Hover me for popover", key="popover_example"):
    um.text("This is popover content")
    um.caption("Additional information here")

um.divider()

# tooltip()
um.subheader("6. tooltip()")
um.tooltip("Hover over this text for a tooltip", help_text="This is the tooltip content!")

um.divider()

# status()
um.subheader("7. status()")
with um.status("Processing your request...", state="running"):
    um.text("Step 1: Validated input")
    um.text("Step 2: Processing data")

with um.status("Complete!", state="complete"):
    um.text("All tasks finished")

um.divider()

um.success("Container components test completed!")
