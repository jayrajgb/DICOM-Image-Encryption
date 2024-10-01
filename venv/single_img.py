import pydicom
import numpy as np
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio
from scipy.stats import entropy


# Function to display DICOM image
def display_dicom_image(pixel_data, title):
    plt.imshow(pixel_data, cmap='gray')
    plt.title(title)
    plt.show()


# Function to calculate and display PSNR and entropy
def calculate_and_display_metrics(original_image, encrypted_image):
    psnr_value = peak_signal_noise_ratio(original_image, encrypted_image)
    entropy_value = entropy(encrypted_image, base=2)

    print(f'PSNR: {psnr_value:.2f}')
    print(f'Entropy: {entropy_value:.2f}')


# Load your original DICOM image
file_path = r"C:\Jayraj\VIT PUNE\TY\EDI\pyDicom\venv\images\1.dcm"
dcm = pydicom.dcmread(file_path)
original_image = dcm.pixel_array

# Convert the original image to uint8 for compatibility
original_image = original_image.astype(np.uint8)

# Generate a random encryption key (use a secure method to store this key)
encryption_key = Fernet.generate_key()
fernet = Fernet(encryption_key)

# Convert the original image to bytes for encryption
original_bytes = original_image.tobytes()

# Encrypt the original image
encrypted_bytes = fernet.encrypt(original_bytes)

# Convert the encrypted bytes back to a NumPy array
encrypted_image = np.frombuffer(encrypted_bytes, dtype=np.uint8)

# Create a new DICOM object for the encrypted image
dcm_encrypted = pydicom.Dataset()
dcm_encrypted.PixelData = encrypted_image.tobytes()

# Copy necessary attributes from the original DICOM dataset
dcm_encrypted.Rows = dcm.Rows
dcm_encrypted.Columns = dcm.Columns
dcm_encrypted.SpecificCharacterSet = dcm.SpecificCharacterSet

# Set the transfer syntax attributes as needed (for example, Little Endian, Explicit VR)
dcm_encrypted.is_little_endian = dcm.is_little_endian
dcm_encrypted.is_implicit_VR = dcm.is_implicit_VR

# Save the encrypted DICOM image to a new file
dcm_encrypted.save_as(r"C:\Users\jayra\Downloads\dicom_results\encrypted_dicom.dcm")

# Display the original image
display_dicom_image(original_image, "Original Image")

# Calculate and display PSNR and entropy
calculate_and_display_metrics(original_image, encrypted_image)
