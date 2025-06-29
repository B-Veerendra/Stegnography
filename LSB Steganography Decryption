import cv2
import hashlib
import numpy as np
from google.colab import files

def extract_bit(pixel_value):
    """Extracts the LSB (Least Significant Bit) from a pixel component."""
    return pixel_value & 1

# --- Decryption Process ---

# 1. Upload the encrypted image
print("Please upload the encrypted image (encryptedImage_LSB.png).")
uploaded = files.upload()
if not uploaded:
    print("No file uploaded. Exiting.")
    exit()
image_path = list(uploaded.keys())[0]

# 2. Load the image
img = cv2.imread(image_path)
if img is None:
    print(f"Error: Could not load image from '{image_path}'. Make sure the file exists and is a valid image.")
    exit()
height, width, channels = img.shape

# 3. Get the passcode
password = input("Enter the passcode used during encryption: ")
hashed_password = hashlib.sha256(password.encode()).digest()

# 4. Extract initial bits (for message length and password hash)
extracted_bits = []
initial_bytes_to_extract = 3 + len(hashed_password) # 3 bytes for length, then password hash
initial_bits_to_extract = initial_bytes_to_extract * 8
pixel_count = 0

for r in range(height):
    for c in range(width):
        for ch in range(channels):
            if pixel_count < initial_bits_to_extract:
                extracted_bits.append(extract_bit(img[r, c, ch]))
                pixel_count += 1
            else:
                break
        if pixel_count >= initial_bits_to_extract:
            break
    if pixel_count >= initial_bits_to_extract:
        break

# Convert initial extracted bits to bytes
extracted_bytes = bytearray()
current_byte = 0
bit_in_byte_counter = 0

for bit in extracted_bits:
    current_byte = current_byte | (bit << bit_in_byte_counter)
    bit_in_byte_counter += 1
    if bit_in_byte_counter == 8:
        extracted_bytes.append(current_byte)
        current_byte = 0
        bit_in_byte_counter = 0

# 5. Retrieve the message length
if len(extracted_bytes) < 3:
    print("Error: Not enough data extracted to determine message length. Image might be corrupted or not properly encrypted.")
    exit()

msg_len_bytes = bytes(extracted_bytes[:3])
try:
    msg_len = int.from_bytes(msg_len_bytes, 'big')
except Exception as e:
    print(f"Error converting length bytes: {e}")
    print("This might not be a valid encrypted image.")
    exit()

print(f"Detected message length: {msg_len} characters.")

# 6. Extract the remaining data (message and password hash)
total_data_bytes_expected = 3 + msg_len + len(hashed_password)
total_data_bits_expected = total_data_bytes_expected * 8

# Calculate starting position for further extraction
processed_pixels = pixel_count
start_r = (processed_pixels // channels) // width
start_c = (processed_pixels // channels) % width
start_ch = processed_pixels % channels

for r in range(start_r, height):
    for c in range(start_c if r == start_r else 0, width):
        for ch in range(start_ch if (r == start_r and c == start_c) else 0, channels):
            if pixel_count >= total_data_bits_expected:
                break
            extracted_bits.append(extract_bit(img[r, c, ch]))
            pixel_count += 1
        if pixel_count >= total_data_bits_expected:
            break
    if pixel_count >= total_data_bits_expected:
        break

# Convert all extracted bits to bytes
extracted_bytes = bytearray()
current_byte = 0
bit_in_byte_counter = 0

for bit in extracted_bits:
    current_byte = current_byte | (bit << bit_in_byte_counter)
    bit_in_byte_counter += 1
    if bit_in_byte_counter == 8:
        extracted_bytes.append(current_byte)
        current_byte = 0
        bit_in_byte_counter = 0

# Handle any remaining bits
if bit_in_byte_counter > 0:
    extracted_bytes.append(current_byte)

if len(extracted_bytes) < total_data_bytes_expected:
    print(f"Error: Not enough data in the image to fully decrypt the message.")
    print(f"Expected {total_data_bytes_expected} bytes, but extracted {len(extracted_bytes)} bytes.")
    exit()

# 7. Separate message and embedded password hash
message_bytes_start_index = 3
message_bytes_end_index = 3 + msg_len
embedded_password_hash_start_index = message_bytes_end_index
embedded_password_hash_end_index = embedded_password_hash_start_index + len(hashed_password)

message_bytes = extracted_bytes[message_bytes_start_index : message_bytes_end_index]
embedded_password_hash = bytes(extracted_bytes[embedded_password_hash_start_index : embedded_password_hash_end_index])

# 8. Verify password and decode message
if embedded_password_hash != hashed_password:
    print("❌ Passcode mismatch. The entered passcode is incorrect or the image is corrupted.")
    exit()

try:
    final_message = message_bytes.decode('utf-8')
    print("\n Decrypted Message: ")
    print("---------------------------------")
    print(final_message)
    print("---------------------------------")
except UnicodeDecodeError:
    print("\nError: Could not decode the message. It might be corrupted or encrypted with a different encoding.")
