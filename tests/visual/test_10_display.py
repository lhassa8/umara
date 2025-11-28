"""Comprehensive test for Display components"""
import umara as um

um.set_page_config(page_title="Display Test", layout="wide")

um.title("Display Components Test")

# badge()
um.subheader("1. badge()")
with um.columns(4):
    with um.column():
        um.badge("New", variant="default")
    with um.column():
        um.badge("Success", variant="success")
    with um.column():
        um.badge("Warning", variant="warning")
    with um.column():
        um.badge("Error", variant="error")

um.divider()

# avatar()
um.subheader("2. avatar()")
with um.columns(4):
    with um.column():
        um.avatar(name="John Doe", size="sm")
        um.caption("Small")
    with um.column():
        um.avatar(name="Jane Smith", size="md")
        um.caption("Medium")
    with um.column():
        um.avatar(name="Bob Wilson", size="lg")
        um.caption("Large")
    with um.column():
        um.avatar(src="https://via.placeholder.com/100", size="lg")
        um.caption("With image")

um.divider()

# avatar_group()
um.subheader("3. avatar_group()")
um.avatar_group(
    avatars=[
        {"name": "Alice"},
        {"name": "Bob"},
        {"name": "Charlie"},
        {"name": "Diana"},
        {"name": "Eve"},
    ],
    max=3
)

um.divider()

# stat_card()
um.subheader("4. stat_card()")
with um.columns(3):
    with um.column():
        um.stat_card(
            title="Total Sales",
            value="$24,500",
            icon="dollar",
            trend="+12%",
            trend_direction="up"
        )
    with um.column():
        um.stat_card(
            title="Active Users",
            value="1,234",
            icon="users",
            trend="+5%",
            trend_direction="up"
        )
    with um.column():
        um.stat_card(
            title="Bounce Rate",
            value="32%",
            icon="chart",
            trend="-3%",
            trend_direction="down"
        )

um.divider()

# empty_state()
um.subheader("5. empty_state()")
um.empty_state(
    title="No results found",
    description="Try adjusting your search or filters to find what you're looking for.",
    icon="search",
    action_label="Clear filters",
    action_key="clear_filters"
)

um.divider()

# loading_skeleton()
um.subheader("6. loading_skeleton()")
um.text("Card skeleton:")
um.loading_skeleton(height="100px", width="200px")
um.text("Text skeleton:")
um.loading_skeleton(height="16px", width="80%")
um.loading_skeleton(height="16px", width="60%")
um.loading_skeleton(height="16px", width="70%")

um.divider()

# timeline()
um.subheader("7. timeline()")
um.timeline([
    {"title": "Order Placed", "description": "Your order has been received", "status": "complete"},
    {"title": "Processing", "description": "Order is being processed", "status": "complete"},
    {"title": "Shipped", "description": "Package is on the way", "status": "current"},
    {"title": "Delivered", "description": "Package will be delivered", "status": "pending"},
])

um.divider()

um.success("Display components test completed!")
