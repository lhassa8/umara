"""Comprehensive test for Navigation components"""
import umara as um

um.set_page_config(page_title="Navigation Test", layout="wide")

um.title("Navigation Components Test")

# sidebar()
um.subheader("1. sidebar()")
with um.sidebar():
    um.text("Sidebar content")
    um.button("Sidebar Button", key="sidebar_btn")
    um.divider()
    um.nav_link("Home", icon="home", active=True, key="nav_home")
    um.nav_link("Settings", icon="settings", key="nav_settings")
    um.nav_link("Profile", icon="user", key="nav_profile")

um.divider()

# nav_link() - standalone
um.subheader("2. nav_link()")
um.nav_link("Dashboard", icon="dashboard", href="#dashboard", key="link_dashboard")
um.nav_link("Reports", icon="chart", href="#reports", key="link_reports")
um.nav_link("Users", icon="users", href="#users", active=True, key="link_users")

um.divider()

# breadcrumbs()
um.subheader("3. breadcrumbs()")
um.breadcrumbs([
    {"label": "Home", "href": "/"},
    {"label": "Products", "href": "/products"},
    {"label": "Electronics", "href": "/products/electronics"},
    {"label": "Phones"},
])

um.divider()

# pagination()
um.subheader("4. pagination()")
page = um.pagination(total_pages=10, current_page=3, key="main_pagination")
um.text(f"Current page: {page}")

um.divider()

# steps()
um.subheader("5. steps()")
um.steps(
    steps=["Cart", "Shipping", "Payment", "Review", "Complete"],
    current=2,
    key="checkout_steps"
)

um.divider()

um.success("Navigation components test completed!")
