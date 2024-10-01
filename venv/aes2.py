import pydicom
from cryptography.fernet import Fernet


# Function to encrypt a DICOM file using AES encryption and overwrite the original file
def encrypt_and_overwrite_dicom_file(file_path, encryption_key):
    try:
        # Read the DICOM file as binary data
        with open(file_path, 'rb') as file:
            dicom_data = file.read()

        # Encrypt the DICOM data
        f = Fernet(encryption_key)
        encrypted_data = f.encrypt(dicom_data)

        # Overwrite the original DICOM file with the encrypted data
        with open(file_path, 'wb') as original_file:
            original_file.write(encrypted_data)

        print("DICOM file encrypted and overwritten successfully.")
    except Exception as e:
        print(f"Error encrypting and overwriting DICOM file: {str(e)}")


# Main loop
while True:
    print("\nDICOM Image Encryption Menu:")
    print("1. Encrypt and Overwrite DICOM File")
    print("2. Exit")

    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        file_path = input("Enter the path of the DICOM file to encrypt and overwrite: ")
        encryption_key = Fernet.generate_key()
        encrypt_and_overwrite_dicom_file(file_path, encryption_key)
        print(f"Encryption Key: {encryption_key.hex()}")

    elif choice == "2":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2).")
