import cv2
import hashlib
import numpy as np
from google.colab import files

def embed_bit(pixel_value, bit):
    """Embeds a single bit into the LSB of a pixel component."""
    # Clear the LSB (AND with 0xFE which is 11111110) and then set it to the bit
    return (pixel_value & 0xFE) | bit

def get_bit(value, bit_position):
    """Gets a specific bit from a byte."""
    return (value >> bit_position) & 1

# STEP 1: Upload the image
print("Please upload the image you want to use for encryption.")
uploaded = files.upload()
if not uploaded:
    print("No file uploaded. Exiting.")
    exit()
image_path = list(uploaded.keys())[0]

# STEP 2: Load the image
img = cv2.imread(image_path)

# Check if image loaded correctly
if img is None:
    print(f"Error: Could not load image from '{image_path}'. Make sure the file format is supported and filename is correct.")
    exit()

# STEP 3: Get image dimensions
height, width, channels = img.shape

# STEP 4: Take user inputs
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# STEP 5: Hash the password using SHA-256
hashed_password = hashlib.sha256(password.encode()).digest()

# STEP 6: Prepend message length to the message
# We'll use 3 bytes (24 bits) for length, allowing messages up to ~16 million characters.
msg_len = len(msg)
full_msg = msg.encode('utf-8') # Encode message to bytes for consistent handling
msg_len_bytes = msg_len.to_bytes(3, 'big') # Length in 3 bytes

# Combine length and message
data_to_hide = msg_len_bytes + full_msg + hashed_password # Add password for extra layer (XOR later)

# Check if image is large enough (each pixel channel holds 1 bit of data)
# Each character and password byte requires 8 bits. We embed 1 bit per channel.
# So, 8 channels (approx 2-3 pixels) per byte.
# For 3 length bytes + message bytes + password bytes, we need (len(data_to_hide) * 8) channels.
required_channels = len(data_to_hide) * 8
total_image_channels = height * width * channels

if required_channels > total_image_channels:
    print(f"Image too small to hold the message. Required channels: {required_channels}, Available: {total_image_channels}")
    print("Please use a larger image or a shorter message.")
    exit()

# STEP 7: Embed the combined data into the image using LSB steganography
bit_index = 0 # Tracks which bit of data_to_hide we are currently embedding

# Iterate through pixels
for r in range(height):
    for c in range(width):
        for ch in range(channels): # Iterate through RGB channels (or BGR for OpenCV)
            if bit_index < required_channels:
                byte_index = bit_index // 8
                bit_in_byte_index = bit_index % 8

                # Get the byte from data_to_hide
                current_byte = data_to_hide[byte_index]

                # Get the specific bit to embed from the current_byte
                bit_to_embed = get_bit(current_byte, bit_in_byte_index)

                # Embed the bit into the LSB of the current pixel channel
                img[r, c, ch] = embed_bit(img[r, c, ch], bit_to_embed)
                bit_index += 1
            else:
                break # All data embedded
        if bit_index >= required_channels:
            break
    if bit_index >= required_channels:
        break

# STEP 8: Save the encrypted image
output_filename = "encryptedImage_LSB.png" # Use PNG to avoid lossy compression for LSB steganography
cv2.imwrite(output_filename, img)

# STEP 9: Download the file to your local system
files.download(output_filename)

print(f"✅ \Message has been encoded into '{output_filename}' using LSB steganography and is ready for download.")
print("Remember to use the new decryption script to retrieve your message.")
