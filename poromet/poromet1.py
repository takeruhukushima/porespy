import porespy
import numpy as np
import matplotlib.pyplot as plt
import skimage.io
import os
from datetime import datetime
from skimage.filters import threshold_otsu
import re

# Create output directory if it doesn't exist
output_dir = 'output_data'
os.makedirs(output_dir, exist_ok=True)

# Create timestamped subdirectory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_subdir = os.path.join(output_dir, timestamp)
os.makedirs(output_subdir, exist_ok=True)

# Load the image
image_path = 'input_images/300x/0.5Pa250WTGB1umSi620C24h8N-NaOH30C4h1e-5N-HCl30C1.5h_m006.jpg'  # Replace with the actual image name
image = skimage.io.imread(image_path)

# Get image dimensions
image_height, image_width = image.shape[:2]

# Define pixel size data for different magnifications and image resolutions
pixel_data = {
    (2560, 1920): {
        10: {'px_per_nm': 1008 / 5000, 'unit': 'nm'},
        20: {'px_per_nm': 807 / 2000, 'unit': 'nm'},
        50: {'px_per_nm': 1022 / 1000, 'unit': 'nm'},
        100: {'px_per_nm': 1018 / 500, 'unit': 'nm'},
    },
    (1280, 960): {
        200: {'px_per_nm': 406 / 200, 'unit': 'nm'},
        300: {'px_per_nm': 303 / 100, 'unit': 'nm'},
    }
}

# Set magnification value
magnification = 300

# Get the pixel data for the current image resolution and magnification
resolution_pixel_data = pixel_data.get((image_width, image_height))
if resolution_pixel_data is None:
    raise ValueError(f"Pixel data for image resolution {image_width}x{image_height} is not defined.")

magnification_pixel_data = resolution_pixel_data.get(magnification)
if magnification_pixel_data is None:
    raise ValueError(f"Pixel data for magnification {magnification} and resolution {image_width}x{image_height} is not defined.")

px_per_nm = magnification_pixel_data['px_per_nm']
unit = magnification_pixel_data['unit']
pixel_size_nm = 1 / px_per_nm

# Apply Otsu's thresholding method
# thresh = threshold_otsu(image)
# thresholded_image = image < thresh

# Calculate the pore size distribution on the segmented image
pore_size_distribution = porespy.metrics.pore_size_distribution(image)

# Calculate average pore size
average_pore_size_pixels = np.average(pore_size_distribution.bin_centers, weights=pore_size_distribution.pdf)
average_pore_size_nm = average_pore_size_pixels * pixel_size_nm

# Save results to file
filename = os.path.join(output_subdir, 'pore_size_analysis.txt')
with open(filename, 'w') as f:
    f.write("Pore Size Analysis\n")
    f.write(f"Image Resolution: {image_width}x{image_height} pixels\n")
    f.write(f"Magnification: {magnification}x\n")
    f.write(f"Pixel Size: {pixel_size_nm:.4f} {unit} per pixel\n")
    f.write(f"Average Pore Size: {average_pore_size_nm:.4f} {unit}\n")

    f.write("\nPore Size Distribution (nm)\n")
    f.write("Pore Size (nm)\tProbability Density\n")
    for bin_center, pdf_value in zip(pore_size_distribution.bin_centers, pore_size_distribution.pdf):
        pore_size_nm_calculated = bin_center * pixel_size_nm
        f.write(f"{pore_size_nm_calculated:.4f}\t{pdf_value:.4f}\n")

# Print the results
print("Pore Size Analysis saved to:")
print(filename)

# Save the segmented image
# segmented_image_filename = os.path.join(output_subdir, 'segmented_image.png')
# skimage.io.imsave(segmented_image_filename, thresholded_image.astype(np.uint8) * 255)
