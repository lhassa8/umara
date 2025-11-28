"""Comprehensive test for Media components"""
import umara as um

um.set_page_config(page_title="Media Test", layout="wide")

um.title("Media Components Test")

# image()
um.subheader("1. image()")
um.image(
    "https://via.placeholder.com/400x200?text=Sample+Image",
    caption="Sample placeholder image",
    width=400
)

um.divider()

# image with columns
um.subheader("2. Multiple images in columns")
with um.columns(3):
    with um.column():
        um.image("https://via.placeholder.com/150?text=Image+1", caption="Image 1")
    with um.column():
        um.image("https://via.placeholder.com/150?text=Image+2", caption="Image 2")
    with um.column():
        um.image("https://via.placeholder.com/150?text=Image+3", caption="Image 3")

um.divider()

# video()
um.subheader("3. video()")
um.info("Video component - provide a video URL to display")
# um.video("https://example.com/sample.mp4")  # Uncomment with real video URL

um.divider()

# audio()
um.subheader("4. audio()")
um.info("Audio component - provide an audio URL to display")
# um.audio("https://example.com/sample.mp3")  # Uncomment with real audio URL

um.divider()

# logo()
um.subheader("5. logo()")
um.logo("https://via.placeholder.com/100x50?text=LOGO", link="https://example.com")

um.divider()

# camera_input()
um.subheader("6. camera_input()")
camera_photo = um.camera_input("Take a photo", key="camera")
if camera_photo:
    um.success("Photo captured!")

um.divider()

# audio_input()
um.subheader("7. audio_input()")
audio_recording = um.audio_input("Record audio", key="audio_rec")
if audio_recording:
    um.success("Audio recorded!")

um.divider()

um.success("Media components test completed!")
