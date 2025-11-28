"""Comprehensive test for Basic Input components"""
import umara as um

um.set_page_config(page_title="Basic Inputs Test", layout="wide")

um.title("Basic Input Components Test")

# button()
um.subheader("1. button()")
if um.button("Primary Button", key="btn_primary"):
    um.success("Primary button clicked!")
if um.button("Secondary Button", key="btn_secondary", variant="secondary"):
    um.info("Secondary button clicked!")
if um.button("Disabled Button", key="btn_disabled", disabled=True):
    um.error("This should not appear")

um.divider()

# download_button()
um.subheader("2. download_button()")
um.download_button(
    label="Download Text File",
    data="Hello, this is the file content!",
    file_name="sample.txt",
    mime="text/plain",
    key="download_btn"
)

um.divider()

# link_button()
um.subheader("3. link_button()")
um.link_button("Visit Example.com", url="https://example.com")

um.divider()

# input() / text_input
um.subheader("4. input() / text_input")
name = um.input("Enter your name", key="name_input", placeholder="John Doe")
if name:
    um.text(f"Hello, {name}!")

password = um.input("Enter password", key="password_input", type="password")
if password:
    um.text(f"Password length: {len(password)} characters")

um.divider()

# text_area()
um.subheader("5. text_area()")
bio = um.text_area("Tell us about yourself", key="bio_input", placeholder="Write something...", height=100)
if bio:
    um.text(f"You wrote {len(bio)} characters")

um.divider()

# slider()
um.subheader("6. slider()")
age = um.slider("Select your age", min_value=0, max_value=100, value=25, key="age_slider")
um.text(f"Selected age: {age}")

range_val = um.slider("Select range", min_value=0, max_value=100, value=(20, 80), key="range_slider")
um.text(f"Selected range: {range_val}")

um.divider()

# select_slider()
um.subheader("7. select_slider()")
size = um.select_slider("Select size", options=["XS", "S", "M", "L", "XL"], value="M", key="size_slider")
um.text(f"Selected size: {size}")

um.divider()

# checkbox()
um.subheader("8. checkbox()")
agree = um.checkbox("I agree to the terms", key="terms_check")
um.text(f"Agreed: {agree}")

subscribe = um.checkbox("Subscribe to newsletter", value=True, key="subscribe_check")
um.text(f"Subscribed: {subscribe}")

um.divider()

# toggle()
um.subheader("9. toggle()")
dark_mode = um.toggle("Enable dark mode", key="dark_toggle")
um.text(f"Dark mode: {'On' if dark_mode else 'Off'}")

um.divider()

# radio()
um.subheader("10. radio()")
color = um.radio("Favorite color", options=["Red", "Green", "Blue"], key="color_radio")
um.text(f"Selected: {color}")

um.divider()

# select() / selectbox
um.subheader("11. select() / selectbox")
country = um.select("Select country", options=["USA", "Canada", "UK", "Australia"], key="country_select")
um.text(f"Selected: {country}")

um.divider()

# multiselect()
um.subheader("12. multiselect()")
fruits = um.multiselect("Select fruits", options=["Apple", "Banana", "Orange", "Grape", "Mango"], default=["Apple"], key="fruits_select")
um.text(f"Selected: {fruits}")

um.divider()

um.success("Basic input components test completed!")
