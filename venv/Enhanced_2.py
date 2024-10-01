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

        # Write the encrypted data back to the same file
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

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

        # Write the decrypted data back to the same file
        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print("DICOM file decrypted successfully.")
    except Exception as e:
        print(f"Error decrypting DICOM file: {str(e)}")


# Function to encrypt all DICOM files in a directory and store keys in a text file
def encrypt_dicom_files_in_directory(directory_path):
    key_file = open("encryption_keys.txt", "a")

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.dcm'):
                encryption_key = Fernet.generate_key()
                file_path = os.path.join(root, file)

                # Encrypt the DICOM file
                encrypt_dicom_file(file_path, encryption_key)

                # Store the key in the text file
                key_file.write(f"{file_path}:{encryption_key.hex()}\n")

    key_file.close()
    print("All DICOM files in the directory encrypted and keys stored in encryption_keys.txt")


# Function to decrypt DICOM files using keys from a text file
def decrypt_dicom_files_using_key_file(key_file_path):
    with open(key_file_path, 'r') as key_file:
        lines = key_file.readlines()
        for line in lines:
            file_path, key_hex = line.strip().split(":")
            decryption_key = bytes.fromhex(key_hex)
            decrypt_dicom_file(file_path, decryption_key)

    print("All DICOM files decrypted using keys from encryption_keys.txt")


# Main loop
while True:
    print("\nDICOM Image Encryption/Decryption Menu:")
    print("1. Encrypt DICOM File")
    print("2. Decrypt DICOM File")
    print("3. Encrypt DICOM Files in Directory and Store Keys")
    print("4. Decrypt DICOM Files using Keys from File")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4/5): ")

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
        directory_path = input("Enter the path of the directory containing DICOM files: ")
        encrypt_dicom_files_in_directory(directory_path)

    elif choice == "4":
        key_file_path = "encryption_keys.txt"  # Assuming the key file is in the same directory
        decrypt_dicom_files_using_key_file(key_file_path)

    elif choice == "5":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3/4/5).")
