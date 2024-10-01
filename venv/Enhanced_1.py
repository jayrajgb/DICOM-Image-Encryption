from cryptography.fernet import Fernet
import os
import glob
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import getpass
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes


# Function to derive an encryption key from a password
def derive_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,  # You can adjust the number of iterations
        salt=salt,
        length=32  # AES-256 key length is 32 bytes
    )
    key = kdf.derive(password.encode())
    return key


# Function to generate a random salt
def generate_salt():
    return os.urandom(16)


# Function to encrypt a DICOM file using AES-256 encryption
def encrypt_dicom_file(file_path, key):
    try:
        # Read the DICOM file as binary data
        with open(file_path, 'rb') as file:
            dicom_data = file.read()

        # Encrypt the DICOM data using AES-256
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(dicom_data)

        # Write the encrypted data back to the same file
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print(f"DICOM file '{file_path}' encrypted successfully.")
    except Exception as e:
        print(f"Error encrypting DICOM file '{file_path}': {str(e)}")


# Function to decrypt a DICOM file using AES-256 decryption
def decrypt_dicom_file(file_path, key):
    try:
        # Read the encrypted DICOM file as binary data
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Decrypt the encrypted data using AES-256
        cipher_suite = Fernet(key)
        decrypted_data = cipher_suite.decrypt(encrypted_data)

        # Write the decrypted data back to the same file
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"DICOM file '{file_path}' decrypted successfully.")
    except Exception as e:
        print(f"Error decrypting DICOM file '{file_path}': {str(e)}")


# Main loop
while True:
    print("\nDICOM Image Encryption/Decryption Menu:")
    print("1. Encrypt DICOM Directory")
    print("2. Decrypt DICOM Directory")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        directory = input("Enter the path of the DICOM directory to encrypt: ")
        password = getpass.getpass("Enter the encryption password: ")

        # Generate a random salt for each encryption
        salt = generate_salt()

        for file_path in glob.glob(os.path.join(directory, '*.dcm')):
            key = derive_key_from_password(password, salt)
            encrypt_dicom_file(file_path, key)

        print("DICOM files in the directory encrypted successfully.")

    elif choice == "2":
        directory = input("Enter the path of the DICOM directory to decrypt: ")
        password = getpass.getpass("Enter the decryption password: ")

        for file_path in glob.glob(os.path.join(directory, '*.dcm')):
            # Load the salt used for encryption from a .salt file (if present)
            salt_file = file_path + '.salt'
            if os.path.exists(salt_file):
                with open(salt_file, 'rb') as f:
                    salt = f.read()
            else:
                print(f"Salt file not found for '{file_path}'")
                continue

            key = derive_key_from_password(password, salt)
            decrypt_dicom_file(file_path, key)

        print("DICOM files in the directory decrypted successfully.")

    elif choice == "3":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3).")
