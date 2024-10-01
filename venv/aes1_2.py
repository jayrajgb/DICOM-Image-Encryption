import pydicom
from cryptography.fernet import Fernet
import os


# Function to encrypt a DICOM file using AES encryption
def encrypt_dicom_file(file_path, encryption_key):
    try:
        # Read the DICOM file as binary data
        with open(file_path, 'rb') as file:
            dicom_data = file.read()

        # Encrypt the DICOM data
        f = Fernet(encryption_key)
        encrypted_data = f.encrypt(dicom_data)

        # Overwrite the original file with the encrypted data
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)

        print("DICOM file encrypted successfully.")
    except Exception as e:
        print(f"Error encrypting DICOM file: {str(e)}")


# Function to decrypt a DICOM file using AES decryption
def decrypt_dicom_file(file_path, decryption_key):
    try:
        # Read the encrypted DICOM file as binary data
        with open(file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        # Decrypt the encrypted data
        f = Fernet(decryption_key)
        decrypted_data = f.decrypt(encrypted_data)

        # Overwrite the original encrypted file with the decrypted data
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(decrypted_data)

        print("DICOM file decrypted successfully.")
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
        encryption_key = Fernet.generate_key()
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
