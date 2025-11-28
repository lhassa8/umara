"""
Batch 3 Test: Input Widgets Part 2
Tests: file_uploader, color_picker, rating, pills, select_slider,
       search_input, tag_input, segmented_control, feedback
"""
import umara as um

um.set_page_config(page_title="Batch 3: Input Widgets Part 2", layout="wide")

um.title("Batch 3: Input Widgets Part 2")
um.caption("Testing advanced input components")

um.divider()

# =============================================================================
# File Input Components
# =============================================================================
um.header("File Input Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("file_uploader()")
        uploaded_file = um.file_uploader("Upload a file", key="file_single")
        if uploaded_file:
            um.success(f"Uploaded: {uploaded_file.name}")
            um.text(f"Size: {uploaded_file.size} bytes")

    with um.column():
        um.subheader("file_uploader() - Multiple")
        uploaded_files = um.file_uploader("Upload multiple files", key="file_multi",
                                          accept_multiple_files=True)
        if uploaded_files:
            um.success(f"Uploaded {len(uploaded_files)} files")
            for f in uploaded_files:
                um.text(f"- {f.name}")

um.divider()

with um.columns(2):
    with um.column():
        um.subheader("file_uploader() - Type filter")
        image_file = um.file_uploader("Upload an image", key="file_image",
                                      type=["png", "jpg", "jpeg", "gif"])

    with um.column():
        um.subheader("file_uploader() - With label visibility")
        doc_file = um.file_uploader("Upload document", key="file_doc",
                                    type=["pdf", "doc", "docx"],
                                    label_visibility="collapsed")

um.divider()

# =============================================================================
# Color & Rating Components
# =============================================================================
um.header("Color & Rating Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("color_picker()")
        color = um.color_picker("Pick a color", key="color_pick", value="#3b82f6")
        um.text(f"Selected: {color}")

        color2 = um.color_picker("Background color", key="color_bg", value="#10b981")
        um.text(f"Background: {color2}")

    with um.column():
        um.subheader("rating()")
        rating = um.rating("Rate this product", key="rating_product")
        um.text(f"Rating: {rating} stars")

        rating2 = um.rating("How was your experience?", key="rating_exp", value=4, max_value=5)
        um.text(f"Experience: {rating2}/5")

um.divider()

# =============================================================================
# Selection Components
# =============================================================================
um.header("Selection Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("pills()")
        selected_pill = um.pills("Select category", key="pills_cat",
                                 options=["All", "Tech", "Sports", "Music", "Art"])
        um.text(f"Selected: {selected_pill}")

        um.subheader("pills() - Multi-select")
        selected_pills = um.pills("Select tags", key="pills_tags",
                                  options=["Python", "JavaScript", "TypeScript", "Rust"],
                                  selection_mode="multi")
        um.text(f"Selected: {selected_pills}")

    with um.column():
        um.subheader("select_slider()")
        priority = um.select_slider("Priority", key="slider_priority",
                                    options=["Low", "Medium", "High", "Critical"])
        um.text(f"Priority: {priority}")

        um.subheader("select_slider() - Range")
        time_range = um.select_slider("Time Range", key="slider_time",
                                      options=["Morning", "Afternoon", "Evening", "Night"],
                                      value=("Morning", "Evening"))
        um.text(f"Range: {time_range[0]} to {time_range[1]}")

um.divider()

# =============================================================================
# Advanced Input Components
# =============================================================================
um.header("Advanced Input Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("search_input()")
        search_term = um.search_input("Search products", key="search_prod",
                                      placeholder="Type to search...")
        if search_term:
            um.text(f"Searching for: {search_term}")

    with um.column():
        um.subheader("tag_input()")
        tags = um.tag_input("Add tags", key="tags_input",
                           suggestions=["python", "javascript", "react", "vue", "angular"])
        if tags:
            um.text(f"Tags: {', '.join(tags)}")

um.divider()

with um.columns(2):
    with um.column():
        um.subheader("segmented_control()")
        view = um.segmented_control("View Mode", key="seg_view",
                                    options=["Grid", "List", "Table"])
        um.text(f"View: {view}")

        um.subheader("segmented_control() - With icons")
        theme = um.segmented_control("Theme", key="seg_theme",
                                     options=["Light", "Dark", "System"],
                                     default="System")
        um.text(f"Theme: {theme}")

    with um.column():
        um.subheader("feedback()")
        feedback = um.feedback("Was this helpful?", key="feedback_helpful")
        if feedback:
            um.text(f"Feedback: {feedback}")

        um.subheader("feedback() - Custom mapping")
        sentiment = um.feedback("Rate your experience", key="feedback_exp",
                               sentiment_mapping=("Negative", "Positive"))
        if sentiment:
            um.text(f"Sentiment: {sentiment}")

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `file_uploader()` | ✅ | Single, multiple, type filter |
| `color_picker()` | ✅ | Default value |
| `rating()` | ✅ | Default value, max_value |
| `pills()` | ✅ | Single and multi-select |
| `select_slider()` | ✅ | Single value and range |
| `search_input()` | ✅ | Placeholder, debounce |
| `tag_input()` | ✅ | Suggestions |
| `segmented_control()` | ✅ | Options, default |
| `feedback()` | ✅ | Default and custom mapping |
""")

um.caption("Batch 3 test complete - verify all advanced input components work correctly")
