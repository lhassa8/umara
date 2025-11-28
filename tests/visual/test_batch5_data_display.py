"""
Batch 5 Test: Data Display
Tests: metric, progress, dataframe, table, data_editor, json_viewer,
       stat_card, empty_state, copy_button, badge, avatar, avatar_group
"""
import umara as um

um.set_page_config(page_title="Batch 5: Data Display", layout="wide")

um.title("Batch 5: Data Display Components")
um.caption("Testing data display components")

um.divider()

# =============================================================================
# Metric Components
# =============================================================================
um.header("Metric Components", level=2)

with um.columns(4):
    with um.column():
        um.subheader("metric() - Basic")
        um.metric("Temperature", "72°F")

    with um.column():
        um.subheader("metric() - With delta")
        um.metric("Revenue", "$12,500", delta="12%")

    with um.column():
        um.subheader("metric() - Delta down")
        um.metric("Costs", "$8,200", delta="-5%", delta_color="inverse")

    with um.column():
        um.subheader("metric() - Neutral")
        um.metric("Users", "1,234", delta="0%", delta_color="off")

um.divider()

# =============================================================================
# Progress Components
# =============================================================================
um.header("Progress Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("progress() - Basic")
        um.progress(0.75)
        um.caption("75% complete")

        um.progress(0.33)
        um.caption("33% complete")

    with um.column():
        um.subheader("progress() - With text")
        um.progress(0.5, text="Uploading...")
        um.progress(1.0, text="Complete!")

um.divider()

# =============================================================================
# Data Tables
# =============================================================================
um.header("Data Tables", level=2)

# Sample data
sample_data = [
    {"name": "Alice", "age": 30, "city": "New York", "score": 95},
    {"name": "Bob", "age": 25, "city": "Los Angeles", "score": 88},
    {"name": "Charlie", "age": 35, "city": "Chicago", "score": 92},
    {"name": "Diana", "age": 28, "city": "Houston", "score": 97},
]

with um.columns(2):
    with um.column():
        um.subheader("dataframe()")
        um.dataframe(sample_data)

    with um.column():
        um.subheader("table()")
        um.table(sample_data)

um.divider()

um.subheader("data_editor()")
um.text("Editable table (click cells to edit):")
edited_data = um.data_editor(sample_data, key="data_editor_test")
if edited_data:
    um.json(edited_data)

um.divider()

# =============================================================================
# JSON Viewer
# =============================================================================
um.header("JSON Viewer", level=2)

sample_json = {
    "name": "Umara",
    "version": "0.4.9",
    "features": ["components", "state", "themes"],
    "config": {
        "debug": True,
        "port": 8501
    }
}

with um.columns(2):
    with um.column():
        um.subheader("json()")
        um.json(sample_json)

    with um.column():
        um.subheader("json() - Expanded")
        um.json(sample_json, expanded=True)

um.divider()

# =============================================================================
# Stat Card
# =============================================================================
um.header("Stat Card", level=2)

with um.columns(3):
    with um.column():
        um.stat_card(
            title="Total Users",
            value="12,345",
            delta="+12%",
            delta_type="positive",
            description="vs last month"
        )

    with um.column():
        um.stat_card(
            title="Revenue",
            value="$54,321",
            delta="-3%",
            delta_type="negative",
            trend_label="MoM"
        )

    with um.column():
        um.stat_card(
            title="Conversion",
            value="3.2%",
            delta="0%",
            delta_type="neutral"
        )

um.divider()

# =============================================================================
# Empty State
# =============================================================================
um.header("Empty State", level=2)

with um.columns(2):
    with um.column():
        um.subheader("empty_state() - Basic")
        um.empty_state(
            title="No data yet",
            description="Start by adding some items"
        )

    with um.column():
        um.subheader("empty_state() - With icon")
        um.empty_state(
            title="No results found",
            description="Try adjusting your search",
            icon="search"
        )

um.divider()

# =============================================================================
# Copy Button
# =============================================================================
um.header("Copy Button", level=2)

with um.columns(2):
    with um.column():
        um.subheader("copy_button()")
        um.copy_button("Copy this text!", key="copy_btn1")
        um.text("Click the button above to copy")

    with um.column():
        um.subheader("copy_button() - Custom label")
        um.copy_button("npm install umara", key="copy_btn2", label="Copy command")

um.divider()

# =============================================================================
# Badge Component
# =============================================================================
um.header("Badge Component", level=2)

um.subheader("badge() - Variants")
with um.columns(5):
    with um.column():
        um.badge("Default")
    with um.column():
        um.badge("Success", variant="success")
    with um.column():
        um.badge("Warning", variant="warning")
    with um.column():
        um.badge("Error", variant="error")
    with um.column():
        um.badge("Info", variant="info")

um.subheader("badge() - Sizes")
with um.columns(3):
    with um.column():
        um.badge("Small", size="sm")
    with um.column():
        um.badge("Medium", size="md")
    with um.column():
        um.badge("Large", size="lg")

um.divider()

# =============================================================================
# Avatar Components
# =============================================================================
um.header("Avatar Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("avatar() - Basic")
        um.avatar("https://i.pravatar.cc/150?img=1", name="Alice")
        um.avatar("https://i.pravatar.cc/150?img=2", name="Bob")
        um.avatar("https://i.pravatar.cc/150?img=3", name="Charlie")

        um.subheader("avatar() - Sizes")
        um.avatar("https://i.pravatar.cc/150?img=4", name="Small", size="sm")
        um.avatar("https://i.pravatar.cc/150?img=5", name="Medium", size="md")
        um.avatar("https://i.pravatar.cc/150?img=6", name="Large", size="lg")

    with um.column():
        um.subheader("avatar_group()")
        um.avatar_group([
            {"src": "https://i.pravatar.cc/150?img=7", "name": "User 1"},
            {"src": "https://i.pravatar.cc/150?img=8", "name": "User 2"},
            {"src": "https://i.pravatar.cc/150?img=9", "name": "User 3"},
            {"src": "https://i.pravatar.cc/150?img=10", "name": "User 4"},
            {"src": "https://i.pravatar.cc/150?img=11", "name": "User 5"},
        ], max_display=3)

        um.subheader("avatar() - Fallback")
        um.avatar(name="No Image")  # Should show initials

um.divider()

# =============================================================================
# Loading Skeleton
# =============================================================================
um.header("Loading Skeleton", level=2)

um.subheader("loading_skeleton()")
with um.columns(2):
    with um.column():
        um.loading_skeleton(height="20px", width="100%")
        um.loading_skeleton(height="20px", width="80%")
        um.loading_skeleton(height="20px", width="60%")

    with um.column():
        um.loading_skeleton(height="100px", width="100%")

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `metric()` | ✅ | Basic, delta, delta_color |
| `progress()` | ✅ | Value, text |
| `dataframe()` | ✅ | Display tabular data |
| `table()` | ✅ | Static table |
| `data_editor()` | ✅ | Editable table |
| `json()` | ✅ | JSON viewer, expanded |
| `stat_card()` | ✅ | Full params |
| `empty_state()` | ✅ | Title, description, icon |
| `copy_button()` | ✅ | Text, label |
| `badge()` | ✅ | Variants, sizes |
| `avatar()` | ✅ | Src, name, sizes, fallback |
| `avatar_group()` | ✅ | Multiple avatars, max_display |
| `loading_skeleton()` | ✅ | Height, width |
""")

um.caption("Batch 5 test complete - verify all data display components work correctly")
