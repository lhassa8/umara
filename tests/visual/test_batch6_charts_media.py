"""
Batch 6 Test: Charts & Media
Tests: line_chart, bar_chart, area_chart, pie_chart, scatter_chart, plotly_chart, map,
       image, video, audio
"""
import umara as um

um.set_page_config(page_title="Batch 6: Charts & Media", layout="wide")

um.title("Batch 6: Charts & Media Components")
um.caption("Testing visualization and media components")

um.divider()

# =============================================================================
# Chart Data
# =============================================================================
line_data = [
    {"month": "Jan", "sales": 100, "revenue": 150},
    {"month": "Feb", "sales": 120, "revenue": 180},
    {"month": "Mar", "sales": 150, "revenue": 220},
    {"month": "Apr", "sales": 130, "revenue": 190},
    {"month": "May", "sales": 180, "revenue": 270},
    {"month": "Jun", "sales": 200, "revenue": 300},
]

bar_data = [
    {"category": "A", "value": 30},
    {"category": "B", "value": 45},
    {"category": "C", "value": 25},
    {"category": "D", "value": 60},
    {"category": "E", "value": 35},
]

pie_data = [
    {"name": "Chrome", "value": 65},
    {"name": "Firefox", "value": 15},
    {"name": "Safari", "value": 12},
    {"name": "Edge", "value": 8},
]

scatter_data = [
    {"x": 10, "y": 20, "size": 5},
    {"x": 25, "y": 35, "size": 10},
    {"x": 40, "y": 15, "size": 8},
    {"x": 55, "y": 45, "size": 12},
    {"x": 70, "y": 30, "size": 6},
    {"x": 85, "y": 50, "size": 15},
]

# =============================================================================
# Line & Area Charts
# =============================================================================
um.header("Line & Area Charts", level=2)

with um.columns(2):
    with um.column():
        um.subheader("line_chart()")
        um.line_chart(line_data, x="month", y=["sales", "revenue"])

    with um.column():
        um.subheader("area_chart()")
        um.area_chart(line_data, x="month", y=["sales", "revenue"])

um.divider()

# =============================================================================
# Bar & Pie Charts
# =============================================================================
um.header("Bar & Pie Charts", level=2)

with um.columns(2):
    with um.column():
        um.subheader("bar_chart()")
        um.bar_chart(bar_data, x="category", y="value")

    with um.column():
        um.subheader("pie_chart()")
        um.pie_chart(pie_data, names="name", values="value")

um.divider()

# =============================================================================
# Scatter Chart
# =============================================================================
um.header("Scatter Chart", level=2)

um.subheader("scatter_chart()")
um.scatter_chart(scatter_data, x="x", y="y", size="size")

um.divider()

# =============================================================================
# Plotly Chart
# =============================================================================
um.header("Plotly Chart", level=2)

um.subheader("plotly_chart()")
um.text("Note: Requires plotly to be installed")

# Create a plotly figure if plotly is available
try:
    import plotly.express as px
    import plotly.graph_objects as go

    # Simple plotly figure
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[100, 150, 120, 180]),
        go.Bar(name='Profit', x=['Q1', 'Q2', 'Q3', 'Q4'], y=[30, 45, 35, 55])
    ])
    fig.update_layout(barmode='group', title='Quarterly Performance')
    um.plotly_chart(fig)
except ImportError:
    um.warning("Plotly not installed - skipping plotly_chart test")
    um.code("pip install plotly", language="bash")

um.divider()

# =============================================================================
# Map Component
# =============================================================================
um.header("Map Component", level=2)

um.subheader("map()")
map_data = [
    {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles"},
    {"lat": 41.8781, "lon": -87.6298, "name": "Chicago"},
    {"lat": 29.7604, "lon": -95.3698, "name": "Houston"},
]
um.map(map_data, latitude="lat", longitude="lon")

um.divider()

# =============================================================================
# Media Components
# =============================================================================
um.header("Media Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("image()")
        um.image("https://picsum.photos/400/200", caption="Random image from Picsum")

        um.subheader("image() - With width")
        um.image("https://picsum.photos/200/200", width=150, caption="150px width")

    with um.column():
        um.subheader("video()")
        um.text("Video component (using sample URL):")
        # Using a sample video URL
        um.video("https://www.w3schools.com/html/mov_bbb.mp4")

um.divider()

um.subheader("audio()")
um.text("Audio component (using sample URL):")
# Using a sample audio URL
um.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `line_chart()` | ✅ | x, y, multiple series |
| `bar_chart()` | ✅ | x, y |
| `area_chart()` | ✅ | x, y, multiple series |
| `pie_chart()` | ✅ | names, values |
| `scatter_chart()` | ✅ | x, y, size |
| `plotly_chart()` | ✅ | Plotly figure object |
| `map()` | ✅ | Latitude, longitude data |
| `image()` | ✅ | URL, caption, width |
| `video()` | ✅ | URL source |
| `audio()` | ✅ | URL source |
""")

um.caption("Batch 6 test complete - verify all chart and media components work correctly")
