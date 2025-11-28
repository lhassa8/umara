"""Simple layout test"""
import umara as um

um.set_page_config(page_title="Simple Layout Test", layout="wide")

um.title("Simple Layout Test")

# Basic container
um.subheader("container()")
with um.container():
    um.text("Inside container")

um.divider()

# Basic columns
um.subheader("columns()")
with um.columns(3):
    with um.column():
        um.text("Column 1")
    with um.column():
        um.text("Column 2")
    with um.column():
        um.text("Column 3")

um.divider()

# Basic card
um.subheader("card()")
with um.card(title="Test Card"):
    um.text("Card content")

um.divider()

# Basic tabs
um.subheader("tabs()")
with um.tabs(["Tab 1", "Tab 2"]):
    with um.tab("Tab 1"):
        um.text("Tab 1 content")
    with um.tab("Tab 2"):
        um.text("Tab 2 content")

um.success("Layout test completed!")
