"""Comprehensive test for Layout components"""
import umara as um

um.set_page_config(page_title="Layout Test", layout="wide")

um.title("Layout Components Test")

# container()
um.subheader("1. container()")
with um.container():
    um.text("This is inside a container")
    um.info("Containers help group elements")

um.divider()

# columns()
um.subheader("2. columns()")
with um.columns(3):
    with um.column():
        um.text("Column 1")
        um.button("Button 1", key="col1_btn")
    with um.column():
        um.text("Column 2")
        um.button("Button 2", key="col2_btn")
    with um.column():
        um.text("Column 3")
        um.button("Button 3", key="col3_btn")

um.divider()

# columns with different ratios
um.subheader("3. columns() with ratios")
with um.columns([2, 1, 1]):
    with um.column():
        um.text("Wide column (2x)")
    with um.column():
        um.text("Normal (1x)")
    with um.column():
        um.text("Normal (1x)")

um.divider()

# grid()
um.subheader("4. grid()")
with um.grid(columns=4, gap="16px"):
    for i in range(8):
        um.text(f"Grid item {i+1}")

um.divider()

# card()
um.subheader("5. card()")
with um.card(title="Card Title", subtitle="Card Subtitle"):
    um.text("This is the card content")
    um.button("Card Action", key="card_btn")

um.divider()

# Multiple cards
um.subheader("6. Multiple cards()")
with um.columns(3):
    with um.column():
        with um.card(title="Card 1"):
            um.text("Card 1 content")
    with um.column():
        with um.card(title="Card 2"):
            um.text("Card 2 content")
    with um.column():
        with um.card(title="Card 3"):
            um.text("Card 3 content")

um.divider()

# tabs()
um.subheader("7. tabs()")
with um.tabs(["Tab A", "Tab B", "Tab C"]):
    with um.tab("Tab A"):
        um.text("Content of Tab A")
        um.info("You are viewing Tab A")
    with um.tab("Tab B"):
        um.text("Content of Tab B")
        um.warning("You are viewing Tab B")
    with um.tab("Tab C"):
        um.text("Content of Tab C")
        um.success("You are viewing Tab C")

um.divider()

# divider()
um.subheader("8. divider()")
um.text("Above divider")
um.divider()
um.text("Below divider")

um.divider()

# spacer()
um.subheader("9. spacer()")
um.text("Before spacer")
um.spacer(height="40px")
um.text("After spacer (40px gap)")

um.divider()

um.success("Layout components test completed!")
