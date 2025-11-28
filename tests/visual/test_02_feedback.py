"""Comprehensive test for Feedback components"""
import umara as um

um.set_page_config(page_title="Feedback Test", layout="wide")

um.title("Feedback Components Test")

# success()
um.subheader("1. success()")
um.success("This is a success message!")

um.divider()

# error()
um.subheader("2. error()")
um.error("This is an error message!")

um.divider()

# warning()
um.subheader("3. warning()")
um.warning("This is a warning message!")

um.divider()

# info()
um.subheader("4. info()")
um.info("This is an info message!")

um.divider()

# toast()
um.subheader("5. toast()")
if um.button("Show Toast", key="btn_toast"):
    um.toast("This is a toast notification!")

um.divider()

# exception()
um.subheader("6. exception()")
try:
    raise ValueError("This is a sample exception for testing")
except Exception as e:
    um.exception(e)

um.divider()

# progress()
um.subheader("7. progress()")
um.progress(0.75, text="75% complete")
um.progress(0.25)
um.progress(0.5, text="Half done!")

um.divider()

# spinner()
um.subheader("8. spinner()")
um.spinner(text="Loading...")

um.divider()

# status()
um.subheader("9. status()")
with um.status("Processing...", state="running"):
    um.text("Task 1: Complete")
    um.text("Task 2: In progress...")

um.divider()

um.success("Feedback components test completed!")
