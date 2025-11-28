"""Test modal specifically"""
import umara as um

um.set_page_config(page_title="Modal Test", layout="wide")

um.title("Modal Test")

um.subheader("Testing modal()")
if um.button("Open Modal", key="btn_modal"):
    um.open_modal("test_modal")

with um.modal("test_modal", title="Test Modal"):
    um.text("Modal content!")
    if um.button("Close", key="btn_close"):
        um.close_modal("test_modal")

um.divider()
um.success("Modal test page loaded!")
