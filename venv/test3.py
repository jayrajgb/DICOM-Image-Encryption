import pydicom
from cryptography.fernet import Fernet
import os

# Function to encrypt the pixel data using AES encryption
def encrypt_pixel_data(pixel_data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(pixel_data.tobytes())
    return encrypted_data

# Function to decrypt the pixel data using AES decryption
def decrypt_pixel_data(encrypted_data, key):
    try:
        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        return None

# Main loop
while True:
    print("\nDICOM Image Encryption/Decryption Menu:")
    print("1. Load DICOM File")
    print("2. Encrypt Pixel Data")
    print("3. Decrypt Pixel Data")
    print("4. Save Modified DICOM File")
    print("5. Exit")

    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        file_path = input("Enter the path of the DICOM file: ")

        try:
            dcm = pydicom.dcmread(file_path)
            pixel_data = dcm.pixel_array
            print("DICOM file loaded successfully.")
        except Exception as e:
            print(f"Error loading DICOM file: {str(e)}")

    elif choice == "2":
        if 'pixel_data' in locals():
            encryption_key = Fernet.generate_key()
            encrypted_pixel_data = encrypt_pixel_data(pixel_data, encryption_key)
            dcm.PixelData = encrypted_pixel_data
            print("Pixel data encrypted successfully.")
            print(f"Encryption Key: {encryption_key}")
        else:
            print("Please load a DICOM file first.")

    elif choice == "3":
        if 'pixel_data' in locals():
            encryption_key = input("Enter encryption key: ")
            if len(encryption_key) == 44:  # Assuming Fernet key length
                decrypted_pixel_data = decrypt_pixel_data(pixel_data, encryption_key.encode())
                if decrypted_pixel_data:
                    dcm.PixelData = decrypted_pixel_data
                    print("Pixel data decrypted successfully.")
                else:
                    print("Error decrypting pixel data. Invalid key.")
            else:
                print("Error decrypting pixel data. Invalid key format.")
        else:
            print("Please load a DICOM file first.")

    elif choice == "4":
        if 'dcm' in locals():
            output_file_path = input("Enter the path to save the modified DICOM file: ")
            dcm.save_as(output_file_path)
            print(f"Modified DICOM file saved as {output_file_path}.")
        else:
            print("No DICOM file to save. Please load a DICOM file first.")

    elif choice == "5":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option (1/2/3/4/5).")
