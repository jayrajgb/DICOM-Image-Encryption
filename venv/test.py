import pydicom
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
import os
import base64
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Function to encrypt using AES
def encrypt_aes(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return encrypted_data

# Function to decrypt using AES
def decrypt_aes(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data

# Logistic Map as a basic chaotic function
def logistic_map(x, r):
    return r * x * (1 - x)

# Chaotic key generation
def chaotic_key_generation(seed, r, iterations):
    key = []
    x = seed
    for _ in range(iterations):
        x = logistic_map(x, r)
        key.append(int(x * 255))
    return bytes(key)

# Function to load a DICOM image
def load_dicom_image(file_path):
    dicom_data = pydicom.dcmread(file_path)
    return dicom_data

# Function to save a DICOM image
def save_dicom_image(dicom_data, output_path):
    dicom_data.save_as(output_path)


def plot_image(image_data, title):
    plt.imshow(image_data, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

# Main function
def main():
    while True:
        print("Options:")
        print("1. Encrypt DICOM image")
        print("2. Decrypt DICOM image")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            dicom_file_path = input("Enter the path of the DICOM image to encrypt: ")
            dicom_image = load_dicom_image(dicom_file_path)

            password = input("Enter a password for AES encryption: ").encode()
            chaotic_seed = 0.5
            chaotic_r = 3.9

            # Generate AES key from the password
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32  # Specify the length of the derived key in bytes
            )
            aes_key = base64.urlsafe_b64encode(kdf.derive(password))

            # Encrypt DICOM image data
            encrypted_data = encrypt_aes(dicom_image.PixelData, aes_key)

            # Generate chaotic key
            chaotic_key = chaotic_key_generation(chaotic_seed, chaotic_r, len(encrypted_data))

            # Apply chaotic encryption
            encrypted_data = bytes(a ^ b for a, b in zip(encrypted_data, chaotic_key))

            output_file_path = input("Enter the path to save the encrypted DICOM image: ")
            save_dicom_image(dicom_image, output_file_path)
            print("DICOM image encrypted and saved successfully!")

        elif choice == "2":
            encrypted_dicom_file_path = input("Enter the path of the encrypted DICOM image: ")
            dicom_image = load_dicom_image(encrypted_dicom_file_path)

            password = input("Enter the password used for encryption: ").encode()
            chaotic_seed = float(input("Enter the chaotic seed (e.g., 0.5): "))
            chaotic_r = float(input("Enter the chaotic parameter (e.g., 3.9): "))

            # Generate AES key from the password
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                iterations=100000,
                salt=salt,
                length=32  # Specify the length of the derived key in bytes
            )
            aes_key = base64.urlsafe_b64encode(kdf.derive(password))

            # Decrypt DICOM image data
            encrypted_data = dicom_image.PixelData

            # Generate chaotic key
            chaotic_key = chaotic_key_generation(chaotic_seed, chaotic_r, len(encrypted_data))

            # Apply chaotic decryption
            decrypted_data = bytes(a ^ b for a, b in zip(encrypted_data, chaotic_key))

            # Decrypt using AES
            decrypted_data = decrypt_aes(decrypted_data, aes_key)

            dicom_image.PixelData = decrypted_data

            output_file_path = input("Enter the path to save the decrypted DICOM image: ")
            save_dicom_image(dicom_image, output_file_path)
            print("DICOM image decrypted and saved successfully!")

            original_image = dicom_image.pixel_array
            encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint16)
            encrypted_image = encrypted_image.reshape(original_image.shape)

            plot_image(original_image, "Original DICOM Image")
            plot_image(encrypted_image, "Encrypted DICOM Image")

        elif choice == "3":
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
