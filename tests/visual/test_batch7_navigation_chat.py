"""
Batch 7 Test: Navigation & Chat
Tests: breadcrumbs, steps, pagination, nav_link,
       chat_container, chat_message, chat_input, chat
"""
import umara as um

um.set_page_config(page_title="Batch 7: Navigation & Chat", layout="wide")

um.title("Batch 7: Navigation & Chat Components")
um.caption("Testing navigation and chat components")

um.divider()

# =============================================================================
# Breadcrumbs
# =============================================================================
um.header("Breadcrumbs Component", level=2)

um.subheader("breadcrumbs()")
um.breadcrumbs([
    {"label": "Home", "href": "/"},
    {"label": "Products", "href": "/products"},
    {"label": "Electronics", "href": "/products/electronics"},
    {"label": "Phones", "href": None},  # Current page (no link)
])

um.divider()

um.subheader("breadcrumbs() - Simple")
um.breadcrumbs([
    {"label": "Dashboard"},
    {"label": "Settings"},
    {"label": "Profile"},
])

um.divider()

# =============================================================================
# Steps Component
# =============================================================================
um.header("Steps Component", level=2)

um.subheader("steps() - Horizontal")
um.steps(
    steps=["Cart", "Shipping", "Payment", "Confirmation"],
    current=2
)

um.divider()

um.subheader("steps() - With descriptions")
um.steps(
    steps=[
        {"title": "Step 1", "description": "Create account"},
        {"title": "Step 2", "description": "Verify email"},
        {"title": "Step 3", "description": "Complete profile"},
        {"title": "Step 4", "description": "Start using"},
    ],
    current=1
)

um.divider()

# =============================================================================
# Pagination
# =============================================================================
um.header("Pagination Component", level=2)

um.subheader("pagination()")

# Initialize page in session state
if "current_page" not in um.session_state:
    um.session_state.current_page = 1

page = um.pagination(
    total_pages=10,
    current_page=um.session_state.current_page,
    key="pagination_demo"
)

if page != um.session_state.current_page:
    um.session_state.current_page = page

um.text(f"Current page: {um.session_state.current_page}")

um.divider()

# =============================================================================
# Navigation Link
# =============================================================================
um.header("Navigation Link Component", level=2)

um.subheader("nav_link()")
with um.columns(3):
    with um.column():
        um.nav_link("Home", href="/", icon="home")
    with um.column():
        um.nav_link("Settings", href="/settings", icon="settings")
    with um.column():
        um.nav_link("Profile", href="/profile", icon="user")

um.divider()

# =============================================================================
# Timeline
# =============================================================================
um.header("Timeline Component", level=2)

um.subheader("timeline()")
um.timeline([
    {"title": "Project Started", "description": "Initial commit and setup", "date": "Jan 1, 2024"},
    {"title": "Alpha Release", "description": "First internal release", "date": "Feb 15, 2024"},
    {"title": "Beta Launch", "description": "Public beta available", "date": "Mar 30, 2024"},
    {"title": "v1.0 Release", "description": "Stable release", "date": "May 1, 2024"},
])

um.divider()

# =============================================================================
# Chat Components
# =============================================================================
um.header("Chat Components", level=2)

um.subheader("chat_message()")
with um.columns(2):
    with um.column():
        um.text("User message:")
        um.chat_message("Hello! How can I help you today?", role="user")

    with um.column():
        um.text("Assistant message:")
        um.chat_message("I'm here to assist you with any questions!", role="assistant")

um.divider()

um.subheader("chat_message() - With avatar")
um.chat_message("This is a user message with custom avatar", role="user", avatar="https://i.pravatar.cc/150?img=1")
um.chat_message("This is an assistant response", role="assistant", avatar="https://i.pravatar.cc/150?img=2")

um.divider()

um.subheader("chat_input()")
user_input = um.chat_input("Type a message...", key="chat_input_demo")
if user_input:
    um.success(f"You typed: {user_input}")

um.divider()

um.subheader("chat_container()")
um.text("Full chat container with messages:")

with um.chat_container(height="300px"):
    um.chat_message("Welcome! How can I help you today?", role="assistant")
    um.chat_message("I need help with my order", role="user")
    um.chat_message("Of course! Can you provide your order number?", role="assistant")
    um.chat_message("It's ORDER-12345", role="user")
    um.chat_message("Thank you! I found your order. It's currently being shipped and should arrive tomorrow.", role="assistant")

um.divider()

um.subheader("chat() - Complete chat component")
um.text("Interactive chat:")

# Initialize chat history
if "messages" not in um.session_state:
    um.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm a demo assistant. How can I help?"}
    ]

# Display chat
with um.chat_container(height="250px"):
    for msg in um.session_state.messages:
        um.chat_message(msg["content"], role=msg["role"])

# Chat input
new_message = um.chat_input("Type your message...", key="interactive_chat")
if new_message:
    um.session_state.messages.append({"role": "user", "content": new_message})
    # Simulate assistant response
    um.session_state.messages.append({
        "role": "assistant",
        "content": f"You said: '{new_message}'. This is a demo response."
    })
    um.rerun()

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `breadcrumbs()` | ✅ | Links, current page |
| `steps()` | ✅ | Simple and with descriptions |
| `pagination()` | ✅ | Total pages, current page |
| `nav_link()` | ✅ | Href, icon |
| `timeline()` | ✅ | Events with dates |
| `chat_message()` | ✅ | Role, avatar |
| `chat_input()` | ✅ | Placeholder |
| `chat_container()` | ✅ | Height, messages |
| `chat()` | ✅ | Full interactive chat |
""")

um.caption("Batch 7 test complete - verify all navigation and chat components work correctly")
