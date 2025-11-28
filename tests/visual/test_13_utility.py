"""Comprehensive test for Utility components"""
import umara as um

um.set_page_config(page_title="Utility Test", layout="wide")

um.title("Utility Components Test")

# copy_button()
um.subheader("1. copy_button()")
um.text("Click to copy this text:")
um.copy_button("Hello, World! This text will be copied.", key="copy1")

um.divider()

# html()
um.subheader("2. html()")
um.html("""
<div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h3 style="margin: 0;">Custom HTML Content</h3>
    <p>This is rendered directly as HTML</p>
    <button style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
        Custom Button
    </button>
</div>
""")

um.divider()

# iframe()
um.subheader("3. iframe()")
um.iframe(
    src="https://example.com",
    height=200,
    width="100%"
)

um.divider()

# Forms
um.subheader("4. form() with form_submit_button()")
with um.form("sample_form"):
    name = um.input("Name", key="form_name")
    email = um.input("Email", key="form_email")
    message = um.text_area("Message", key="form_message")
    submitted = um.form_submit_button("Submit Form")
    if submitted:
        um.success(f"Form submitted! Name: {name}, Email: {email}")

um.divider()

# download_button()
um.subheader("5. download_button()")
csv_data = "name,age,city\nAlice,25,NYC\nBob,30,LA\nCharlie,35,Chicago"
um.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="data.csv",
    mime="text/csv",
    key="download_csv"
)

um.divider()

# map()
um.subheader("6. map()")
map_data = [
    {"lat": 40.7128, "lon": -74.0060, "name": "New York"},
    {"lat": 34.0522, "lon": -118.2437, "name": "Los Angeles"},
    {"lat": 41.8781, "lon": -87.6298, "name": "Chicago"},
]
um.map(data=map_data, zoom=3)

um.divider()

um.success("Utility components test completed!")
