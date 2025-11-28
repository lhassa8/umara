"""
Batch 8 Test: Utility & Misc
Tests: download_button, link_button, form, form_submit_button,
       html, iframe, write, write_stream, echo, spinner, status, logo
"""
import umara as um
import time

um.set_page_config(page_title="Batch 8: Utility & Misc", layout="wide")

um.title("Batch 8: Utility & Misc Components")
um.caption("Testing utility and miscellaneous components")

um.divider()

# =============================================================================
# Download & Link Buttons
# =============================================================================
um.header("Download & Link Buttons", level=2)

with um.columns(2):
    with um.column():
        um.subheader("download_button()")
        um.download_button(
            label="Download Text File",
            data="Hello, this is the file content!",
            file_name="hello.txt",
            mime="text/plain",
            key="download_txt"
        )

        um.download_button(
            label="Download CSV",
            data="name,age,city\nAlice,30,NYC\nBob,25,LA",
            file_name="data.csv",
            mime="text/csv",
            key="download_csv"
        )

    with um.column():
        um.subheader("link_button()")
        um.link_button("Open Google", url="https://google.com", key="link_google")
        um.link_button("Open GitHub", url="https://github.com", key="link_github")

um.divider()

# =============================================================================
# Form Components
# =============================================================================
um.header("Form Components", level=2)

um.subheader("form() with form_submit_button()")

with um.form("contact_form", clear_on_submit=True):
    name = um.input("Name", key="form_name")
    email = um.input("Email", key="form_email", type="email")
    message = um.text_area("Message", key="form_message")

    submitted = um.form_submit_button("Submit Form")

    if submitted:
        um.success(f"Form submitted! Name: {name}, Email: {email}")
        um.text(f"Message: {message}")

um.divider()

um.subheader("form() - Without clear_on_submit")

with um.form("settings_form"):
    theme = um.select("Theme", options=["Light", "Dark", "System"], key="form_theme")
    notifications = um.checkbox("Enable notifications", key="form_notif")

    if um.form_submit_button("Save Settings"):
        um.success(f"Settings saved! Theme: {theme}, Notifications: {notifications}")

um.divider()

# =============================================================================
# HTML & Iframe
# =============================================================================
um.header("HTML & Iframe Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("html()")
        um.html("""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin: 0;">Custom HTML Content</h3>
            <p style="margin: 10px 0 0 0;">Rendered directly in the page</p>
        </div>
        """)

    with um.column():
        um.subheader("iframe()")
        um.iframe(
            src="https://www.openstreetmap.org/export/embed.html?bbox=-0.1,51.5,-0.05,51.52&layer=mapnik",
            height="200px",
            title="OpenStreetMap"
        )

um.divider()

# =============================================================================
# Write Components
# =============================================================================
um.header("Write Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("write()")
        um.write("This is a string")
        um.write(42)
        um.write(3.14159)
        um.write(["list", "of", "items"])
        um.write({"key": "value", "number": 123})

    with um.column():
        um.subheader("write() - Complex objects")
        um.write({
            "nested": {
                "data": [1, 2, 3],
                "flag": True
            }
        })

um.divider()

um.subheader("write_stream()")
um.text("Streaming text demonstration:")

def generate_stream():
    """Generator that yields text chunks"""
    words = "This is a streaming text demonstration that shows content appearing word by word.".split()
    for word in words:
        yield word + " "
        time.sleep(0.1)

if um.button("Start Stream", key="btn_stream"):
    um.write_stream(generate_stream())

um.divider()

# =============================================================================
# Echo Component
# =============================================================================
um.header("Echo Component", level=2)

um.subheader("echo()")
um.text("The echo component shows code and its output:")

with um.echo():
    x = 10
    y = 20
    result = x + y
    um.text(f"The result of {x} + {y} = {result}")

um.divider()

# =============================================================================
# Spinner & Status
# =============================================================================
um.header("Spinner & Status Components", level=2)

with um.columns(2):
    with um.column():
        um.subheader("spinner()")
        if um.button("Show Spinner", key="btn_spinner"):
            with um.spinner("Loading..."):
                time.sleep(2)
            um.success("Done!")

    with um.column():
        um.subheader("status()")
        um.status("online", "Server is running")
        um.status("offline", "Database disconnected")
        um.status("busy", "Processing request")

um.divider()

# =============================================================================
# Logo Component
# =============================================================================
um.header("Logo Component", level=2)

um.subheader("logo()")
um.logo(
    image="https://raw.githubusercontent.com/streamlit/streamlit/develop/frontend/app/src/assets/favicon.png",
    link="https://github.com"
)

um.divider()

# =============================================================================
# Test Summary
# =============================================================================
um.header("Test Summary", level=2)

um.markdown("""
### Components Tested:

| Component | Status | Notes |
|-----------|--------|-------|
| `download_button()` | ✅ | Data, file_name, mime |
| `link_button()` | ✅ | URL, label |
| `form()` | ✅ | clear_on_submit |
| `form_submit_button()` | ✅ | Inside form |
| `html()` | ✅ | Raw HTML content |
| `iframe()` | ✅ | Src, height, title |
| `write()` | ✅ | Various data types |
| `write_stream()` | ✅ | Generator streaming |
| `echo()` | ✅ | Code and output |
| `spinner()` | ✅ | Loading indicator |
| `status()` | ✅ | Status indicators |
| `logo()` | ✅ | Image, link |
""")

um.caption("Batch 8 test complete - verify all utility components work correctly")
