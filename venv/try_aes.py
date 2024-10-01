import pydicom
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import shutil

# Function to generate a random AES key
def generate_aes_key():
    return os.urandom(32)

# Function to encrypt a DICOM file using AES encryption and save as a new file
def encrypt_dicom_file(file_path, encryption_key):
    try:
        # Generate an IV (Initialization Vector)
        iv = os.urandom(16)

        # Create a cipher object for AES encryption
        cipher = Cipher(algorithms.AES(encryption_key), modes.CFB(iv))

        # Read the DICOM file as binary data
        with open(file_path, 'rb') as file:
            dicom_data = file.read()

        # Create an encryptor
        encryptor = cipher.encryptor()

        # Encrypt the DICOM data
        encrypted_data = encryptor.update(dicom_data) + encryptor.finalize()

        # Write the encrypted data to a new file
        with open('encrypted_dicom_file.dcm', 'wb') as encrypted_file:
            encrypted_file.write(iv + encrypted_data)

        print("DICOM file encrypted and saved as 'encrypted_dicom_file.dcm'.")
    except Exception as e:
        print(f"Error encrypting DICOM file: {str(e)}")

# Function to decrypt a DICOM file using AES decryption and save as a new file
def decrypt_dicom_file(file_path, decryption_key):
    try:
        # Read the encrypted DICOM file as binary data
        with open(file_path, 'rb') as encrypted_file:
            iv = encrypted_file.read(16)  # Read the IV
            encrypted_data = encrypted_file.read()

        # Create a cipher object for AES decryption
        cipher = Cipher(algorithms.AES(decryption_key), modes.CFB(iv))

        # Create a decryptor
        decryptor = cipher.decryptor()

        # Decrypt the encrypted data
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Write the decrypted data to a new file
        with open('decrypted_dicom_file.dcm', 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print("DICOM file decrypted and saved as 'decrypted_dicom_file.dcm'.")
    except Exception as e:
        print(f"Error decrypting DICOM file: {str(e)}")

# Main loop
while True:
    print("\nDICOM Image Encryption/Decryption Menu:")
    print("1. Encrypt DICOM File")
    print("2. Decrypt DICOM File")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        file_path = input("Enter the path of the DICOM file to encrypt: ")
        encryption_key = generate_aes_key()
        encrypt_dicom_file(file_path, encryption_key)
        print(f"Encryption Key: {encryption_key.hex()}")

    elif choice == "2":
        file_path = input("Enter the path of the encrypted DICOM file to decrypt: ")
        decryption_key = input("Enter the decryption key (hexadecimal): ")
        decryption_key = bytes.fromhex(decryption_key)
        decrypt_dicom_file(file_path, decryption_key)

    elif choice == "3":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3).")
