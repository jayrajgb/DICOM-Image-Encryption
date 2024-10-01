import tkinter as tk
from tkinter import filedialog
import os

# Import the DICOM encryption/decryption functions from the other script
from dicom_crypto import generate_aes_key, encrypt_dicom_file, decrypt_dicom_file

# Function to handle the "Encrypt" button click
def encrypt_file():
    file_path = file_entry.get()
    if os.path.isfile(file_path):
        encryption_key = generate_aes_key()
        encrypt_dicom_file(file_path, encryption_key)
        encryption_key_label.config(text=f"Encryption Key: {encryption_key.hex()}")
    else:
        encryption_key_label.config(text="Invalid file path")

# Function to handle the "Decrypt" button click
def decrypt_file():
    file_path = file_entry.get()
    decryption_key = decryption_key_entry.get()
    decryption_key = bytes.fromhex(decryption_key)
    decrypt_dicom_file(file_path, decryption_key)

# Create the main application window
app = tk.Tk()
app.title("DICOM Image Encryption/Decryption")

# Create and configure GUI elements
file_label = tk.Label(app, text="Enter the path of the DICOM file:")
file_entry = tk.Entry(app)
encrypt_button = tk.Button(app, text="Encrypt", command=encrypt_file)
decrypt_button = tk.Button(app, text="Decrypt", command=decrypt_file)
decryption_key_label = tk.Label(app, text="Decryption Key (hexadecimal):")
decryption_key_entry = tk.Entry(app)

# Place GUI elements on the window
file_label.pack()
file_entry.pack()
encrypt_button.pack()
decrypt_button.pack()
decryption_key_label.pack()
decryption_key_entry.pack()

# Start the GUI main loop
app.mainloop()
