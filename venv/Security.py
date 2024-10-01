import pydicom
from cryptography.fernet import Fernet
import os
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.measure import shannon_entropy


# Function to calculate NPCR and UACI from binary data
def calculate_npcr_uaci(original_data, encrypted_data):
    original_image = np.frombuffer(original_data, dtype=np.uint8)
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)
    npcr = np.mean(original_image != encrypted_image)
    uaci = np.mean(np.abs(original_image - encrypted_image))
    return npcr, uaci

# Function to calculate PSNR from binary data
def calculate_psnr(original_data, encrypted_data):
    original_image = np.frombuffer(original_data, dtype=np.uint8)
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)
    mse = np.mean((original_image - encrypted_image) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255
    psnr_value = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr_value

# Function to calculate entropy from binary data
def calculate_entropy(encrypted_data):
    encrypted_image = np.frombuffer(encrypted_data, dtype=np.uint8)
    entropy_value = shannon_entropy(encrypted_image)
    return entropy_value

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
def encrypt_dicom_files_in_directory(directory_path, key_file_path):
    key_file = open(key_file_path, "a")

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
    print("All DICOM files in the directory encrypted and keys stored in text file.")


# Function to decrypt DICOM files using keys from a text file
def decrypt_dicom_files_using_key_file(key_file_path):
    with open(key_file_path, 'r') as key_file:
        lines = key_file.readlines()
        for line in lines:
            file_path, key_hex = line.strip().split(":")
            decryption_key = bytes.fromhex(key_hex)
            decrypt_dicom_file(file_path, decryption_key)

    # Delete the key file after decrypting all images
    os.remove(key_file_path)
    print("All DICOM files decrypted using keys from the text file.")

# Main loop
while True:
    print("\nDICOM Image Encryption/Decryption Menu:")
    print("1. Encrypt DICOM File")
    print("2. Decrypt DICOM File")
    print("3. Encrypt DICOM Files in Directory and Store Keys")
    print("4. Decrypt DICOM Files using Keys from File")
    print("5. Perform Security Analysis")
    print("6. Exit")

    choice = input("Enter your choice (1/2/3/4/5/6): ")

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
        key_file_path = input("Enter the path to create the key file: ")
        encrypt_dicom_files_in_directory(directory_path, key_file_path)

    elif choice == "4":
        key_file_path = input("Enter the path of the key file containing decryption keys: ")
        decrypt_dicom_files_using_key_file(key_file_path)

    elif choice == "5":
        original_file_path = input("Enter the path of the original DICOM file: ")
        encrypted_file_path = input("Enter the path of the encrypted DICOM file: ")

        with open(original_file_path, 'rb') as original_file:
            original_data = original_file.read()

        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        npcr, uaci = calculate_npcr_uaci(original_data, encrypted_data)
        print(f"NPCR: {npcr}")
        print(f"UACI: {uaci}")

        psnr_value = calculate_psnr(original_data, encrypted_data)
        print(f"PSNR: {psnr_value} dB")

        entropy_value = calculate_entropy(encrypted_data)
        print(f"Entropy: {entropy_value}")

    elif choice == "6":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3/4/5/6).")
