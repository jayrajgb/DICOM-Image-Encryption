import pydicom
from PIL import Image

# Load a DICOM image
dicom_file = "your_dicom_image.dcm"
ds = pydicom.dcmread(dicom_file)

# Simple XOR encryption for demonstration purposes
key = 0xAA
encrypted_pixel_data = ds.pixel_array ^ key

# Create a copy of the original DICOM dataset
encrypted_ds = ds.copy()

# Replace the pixel data with the encrypted data
encrypted_ds.PixelData = encrypted_pixel_data.tobytes()

# Save the encrypted DICOM image
encrypted_ds.save_as("encrypted_dicom_image.dcm")

# Display the original and encrypted images side by side
original_image = Image.fromarray(ds.pixel_array)
encrypted_image = Image.fromarray(encrypted_pixel_data)

original_image.show(title="Original DICOM Image")
encrypted_image.show(title="Encrypted DICOM Image")
