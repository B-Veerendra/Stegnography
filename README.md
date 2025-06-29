# 🕵️‍♂️ Image Steganography using Python

This project allows you to **hide secret messages inside image files** using a simple form of steganography. The message is encrypted using a password-based SHA-256 hash, and embedded into the pixel values of an image. You can later decrypt the message using the same password.

---

## 📌 Features

- 🔐 Password-protected encryption & decryption
- 🔒 SHA-256 based key hashing
- 🖼️ Works with `.jpg` and `.png` images
- 📥 Clean and simple CLI interaction
- 💡 Educational, beginner-friendly code

---


## ⚙️ Requirements

Python 3.x
OpenCV (cv2)

Google Colab (optional)

Install dependencies:

bash
Copy
Edit
pip install opencv-python

## 🚀 How to Use

### 🔐 Encryption
Run encrypt.py.

Upload an image (e.g., input.jpg).

Enter the secret message.

Enter a password.

The script will save encryptedImage.jpg with the hidden message.

bash
Copy
Edit
python encrypt.py

### 🔓 Decryption
Run decrypt.py.

Upload encryptedImage.jpg.

Enter the same password used during encryption.

The secret message will be displayed in the output.

bash
Copy
Edit
python decrypt.py

### 💡 Example
Hidden Message:

pgsql
Copy
Edit
The treasure is buried under the old oak tree. ~END~
Decrypted Output:

pgsql
Copy
Edit
The treasure is buried under the old oak tree.

### 🧪 How It Works
The password is hashed with SHA-256 to generate a key.

Each character in the message is converted to ASCII and encrypted using a modulo operation with the hashed key.

The resulting values are embedded into the RGB values of image pixels.

During decryption, the process is reversed using the same password.

## 📚 References
Wikipedia: Steganography

Python hashlib docs

OpenCV Python Docs

