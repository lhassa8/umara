"""
Batch 2 Test: Input Widgets Part 1
Tests: button, input, text_area, number_input, slider, select,
       multiselect, checkbox, toggle, radio, date_input, time_input
"""
import umara as um
from datetime import date, time

um.set_page_config(page_title="Batch 2: Input Widgets Part 1", layout="wide")

um.title("Batch 2: Input Widgets Part 1")
um.caption("Testing basic input components")

um.divider()

# =============================================================================
# Button Components
# =============================================================================
um.header("Button Components", level=2)

with um.columns(3):
    with um.column():
        um.subheader("button() - Basic")
        if um.button("Primary Button", key="btn_primary"):
            um.success("Primary clicked!")
        if um.button("Secondary", key="btn_secondary", variant="secondary"):
            um.info("Secondary clicked!")
        if um.button("Outline", key="btn_outline", variant="outline"):
            um.info("Outline clicked!")

    with um.column():
        um.subheader("button() - With Icons")
        if um.button("Save", key="btn_save", icon="save"):
            um.success("Saved!")
        if um.button("Delete", key="btn_delete", icon="trash", variant="destructive"):
            um.warning("Delete clicked!")
        um.button("Disabled", key="btn_disabled", disabled=True)

    with um.column():
        um.subheader("button() - Variants")
        if um.button("Ghost", key="btn_ghost", variant="ghost"):
            um.info("Ghost clicked!")
        if um.button("Link Style", key="btn_link", variant="link"):
            um.info("Link clicked!")

um.divider()

# =============================================================================
# Text Input Components
# =============================================================================
um.header("Text Input Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("input()")
        name = um.input("Your Name", key="input_name", placeholder="Enter your name")
        if name:
            um.text(f"Hello, {name}!")

        email = um.input("Email", key="input_email", type="email", placeholder="user@example.com")
        password = um.input("Password", key="input_password", type="password")

        um.subheader("input() - With max_chars")
        limited = um.input("Limited (10 chars)", key="input_limited", max_chars=10)

    with um.column():
        um.subheader("text_area()")
        bio = um.text_area("Biography", key="textarea_bio", placeholder="Tell us about yourself...", height=100)
        if bio:
            um.caption(f"Character count: {len(bio)}")

        um.subheader("text_area() - With max_chars")
        short_bio = um.text_area("Short Bio (100 chars max)", key="textarea_short", max_chars=100, height=80)

um.divider()

# =============================================================================
# Number Input Components
# =============================================================================
um.header("Number Input Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("number_input()")
        age = um.number_input("Age", key="num_age", min_value=0, max_value=150, value=25)
        um.text(f"Your age: {age}")

        price = um.number_input("Price", key="num_price", min_value=0.0, max_value=1000.0, value=9.99, step=0.01)
        um.text(f"Price: ${price:.2f}")

    with um.column():
        um.subheader("slider()")
        volume = um.slider("Volume", key="slider_volume", min_value=0, max_value=100, value=50)
        um.text(f"Volume: {volume}%")

        um.subheader("slider() - Range")
        price_range = um.slider("Price Range", key="slider_range", min_value=0, max_value=1000, value=(100, 500))
        um.text(f"Range: ${price_range[0]} - ${price_range[1]}")

um.divider()

# =============================================================================
# Select Components
# =============================================================================
um.header("Select Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("select()")
        color = um.select("Favorite Color", key="select_color", options=["Red", "Green", "Blue", "Yellow"])
        if color:
            um.text(f"Selected: {color}")

        um.subheader("select() - With index")
        size = um.select("Size", key="select_size", options=["Small", "Medium", "Large"], index=1)
        um.text(f"Size: {size}")

    with um.column():
        um.subheader("multiselect()")
        fruits = um.multiselect("Select Fruits", key="multiselect_fruits",
                                options=["Apple", "Banana", "Cherry", "Date", "Elderberry"])
        if fruits:
            um.text(f"Selected: {', '.join(fruits)}")

        um.subheader("multiselect() - With default")
        tags = um.multiselect("Tags", key="multiselect_tags",
                              options=["Python", "JavaScript", "TypeScript", "Rust", "Go"],
                              default=["Python"])

um.divider()

# =============================================================================
# Boolean Input Components
# =============================================================================
um.header("Boolean Input Components", level=2)

with um.columns(3):
    with um.column():
        um.subheader("checkbox()")
        agree = um.checkbox("I agree to terms", key="checkbox_agree")
        um.text(f"Agreed: {agree}")

        newsletter = um.checkbox("Subscribe to newsletter", key="checkbox_news", value=True)
        um.text(f"Subscribed: {newsletter}")

    with um.column():
        um.subheader("toggle()")
        dark_mode = um.toggle("Dark Mode", key="toggle_dark")
        um.text(f"Dark Mode: {'On' if dark_mode else 'Off'}")

        notifications = um.toggle("Notifications", key="toggle_notif", value=True)
        um.text(f"Notifications: {'On' if notifications else 'Off'}")

    with um.column():
        um.subheader("radio()")
        plan = um.radio("Select Plan", key="radio_plan", options=["Free", "Pro", "Enterprise"])
        um.text(f"Selected Plan: {plan}")

um.divider()

# =============================================================================
# Date/Time Input Components
# =============================================================================
um.header("Date/Time Input Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("date_input()")
        selected_date = um.date_input("Select Date", key="date_input")
        um.text(f"Selected: {selected_date}")

        um.subheader("date_input() - With min/max")
        birth_date = um.date_input("Birth Date", key="date_birth",
                                   min_value=date(1900, 1, 1),
                                   max_value=date.today())

    with um.column():
        um.subheader("time_input()")
        selected_time = um.time_input("Select Time", key="time_input")
        um.text(f"Selected: {selected_time}")

        um.subheader("time_input() - With step")
        meeting_time = um.time_input("Meeting Time", key="time_meeting", step=900)  # 15 min steps

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `button()` | ✅ | Variants, icons, disabled |
| `input()` | ✅ | Types, placeholder, max_chars |
| `text_area()` | ✅ | Height, max_chars |
| `number_input()` | ✅ | Min/max, step, float values |
| `slider()` | ✅ | Single value and range |
| `select()` | ✅ | Options, index |
| `multiselect()` | ✅ | Options, default selection |
| `checkbox()` | ✅ | Default value |
| `toggle()` | ✅ | Default value |
| `radio()` | ✅ | Options |
| `date_input()` | ✅ | Min/max dates |
| `time_input()` | ✅ | Step intervals |
""")

um.caption("Batch 2 test complete - verify all input components work correctly")
