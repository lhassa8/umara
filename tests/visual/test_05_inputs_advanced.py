"""Comprehensive test for Advanced Input components"""
import umara as um
from datetime import date, time

um.set_page_config(page_title="Advanced Inputs Test", layout="wide")

um.title("Advanced Input Components Test")

# number_input()
um.subheader("1. number_input()")
quantity = um.number_input("Quantity", min_value=0, max_value=100, value=10, step=1, key="quantity_input")
um.text(f"Quantity: {quantity}")

price = um.number_input("Price", min_value=0.0, max_value=1000.0, value=29.99, step=0.01, key="price_input")
um.text(f"Price: ${price}")

um.divider()

# date_input()
um.subheader("2. date_input()")
birthday = um.date_input("Birthday", value=date(1990, 1, 15), key="birthday_input")
um.text(f"Birthday: {birthday}")

event_date = um.date_input(
    "Event date",
    min_date=date(2024, 1, 1),
    max_date=date(2025, 12, 31),
    key="event_date_input"
)
um.text(f"Event: {event_date}")

um.divider()

# time_input()
um.subheader("3. time_input()")
meeting_time = um.time_input("Meeting time", value=time(14, 30), key="meeting_time_input")
um.text(f"Meeting at: {meeting_time}")

um.divider()

# file_uploader()
um.subheader("4. file_uploader()")
uploaded_file = um.file_uploader(
    "Upload a file",
    type=["txt", "pdf", "png", "jpg"],
    key="file_upload"
)
if uploaded_file:
    um.success(f"File uploaded: {uploaded_file}")

um.divider()

# Multiple file upload
um.subheader("5. file_uploader() - Multiple files")
uploaded_files = um.file_uploader(
    "Upload multiple files",
    type=["txt", "csv"],
    accept_multiple_files=True,
    key="files_upload"
)
if uploaded_files:
    um.success(f"Files uploaded: {len(uploaded_files)} files")

um.divider()

# color_picker()
um.subheader("6. color_picker()")
color = um.color_picker("Pick a color", value="#FF5733", key="color_picker")
um.text(f"Selected color: {color}")

um.divider()

# rating()
um.subheader("7. rating()")
rating = um.rating("Rate this app", max_value=5, value=4, key="rating_input")
um.text(f"Rating: {rating} / 5")

um.divider()

# search_input()
um.subheader("8. search_input()")
search = um.search_input("Search...", key="search_input")
if search:
    um.text(f"Searching for: {search}")

um.divider()

# tag_input()
um.subheader("9. tag_input()")
tags = um.tag_input("Add tags", value=["python", "ui"], key="tag_input")
um.text(f"Tags: {tags}")

um.divider()

# pills()
um.subheader("10. pills()")
selected_pill = um.pills("Options", options=["Option A", "Option B", "Option C"], key="pills_input")
um.text(f"Selected: {selected_pill}")

um.divider()

# segmented_control()
um.subheader("11. segmented_control()")
segment = um.segmented_control("View mode", options=["List", "Grid", "Table"], key="segment_input")
um.text(f"View mode: {segment}")

um.divider()

um.success("Advanced input components test completed!")
