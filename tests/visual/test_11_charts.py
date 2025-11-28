"""Comprehensive test for Chart components"""
import umara as um

um.set_page_config(page_title="Charts Test", layout="wide")

um.title("Chart Components Test")

# Sample data for charts
line_data = [
    {"month": "Jan", "sales": 100, "revenue": 200},
    {"month": "Feb", "sales": 150, "revenue": 280},
    {"month": "Mar", "sales": 200, "revenue": 350},
    {"month": "Apr", "sales": 180, "revenue": 320},
    {"month": "May", "sales": 250, "revenue": 420},
    {"month": "Jun", "sales": 300, "revenue": 500},
]

bar_data = [
    {"category": "A", "value": 40},
    {"category": "B", "value": 65},
    {"category": "C", "value": 30},
    {"category": "D", "value": 85},
    {"category": "E", "value": 55},
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
    {"x": 40, "y": 28, "size": 8},
    {"x": 55, "y": 60, "size": 12},
    {"x": 70, "y": 45, "size": 7},
    {"x": 85, "y": 75, "size": 15},
]

# line_chart()
um.subheader("1. line_chart()")
um.line_chart(data=line_data, x="month", y=["sales", "revenue"], height=300)

um.divider()

# bar_chart()
um.subheader("2. bar_chart()")
um.bar_chart(data=bar_data, x="category", y="value", height=300)

um.divider()

# area_chart()
um.subheader("3. area_chart()")
um.area_chart(data=line_data, x="month", y="sales", height=300)

um.divider()

# pie_chart()
um.subheader("4. pie_chart()")
um.pie_chart(data=pie_data, names="name", values="value", height=300)

um.divider()

# scatter_chart()
um.subheader("5. scatter_chart()")
um.scatter_chart(data=scatter_data, x="x", y="y", size="size", height=300)

um.divider()

# Multiple charts in columns
um.subheader("6. Charts in columns")
with um.columns(2):
    with um.column():
        um.text("Bar Chart")
        um.bar_chart(data=bar_data, x="category", y="value", height=200)
    with um.column():
        um.text("Pie Chart")
        um.pie_chart(data=pie_data, names="name", values="value", height=200)

um.divider()

um.success("Chart components test completed!")
