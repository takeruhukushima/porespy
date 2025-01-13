import porespy
import numpy as np
import matplotlib.pyplot as plt
import skimage.io
import os
from datetime import datetime
from skimage.filters import threshold_otsu

# Create output directory if it doesn't exist
output_dir = 'output_data'
os.makedirs(output_dir, exist_ok=True)

# Create timestamped subdirectory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_subdir = os.path.join(output_dir, timestamp)
os.makedirs(output_subdir, exist_ok=True)

# Load the image
image_path = 'input_images/ダウンロード.jpg'  # Replace with the actual image name
image = skimage.io.imread(image_path)

# Set the resolution: 600 nm = 100 pixels
pixel_size_nm = 600 / 100  # nm per pixel

# Apply Otsu's thresholding method
thresh = threshold_otsu(image)
thresholded_image = image < thresh

# Calculate the pore size distribution BEFORE threshold adjustment
pore_size_distribution_before = porespy.metrics.pore_size_distribution(image)

# Save results before threshold adjustment to file
filename_before = os.path.join(output_subdir, 'pore_size_distribution_before.txt')
with open(filename_before, 'w') as f_before:
    f_before.write("Pore Size Distribution Before Threshold Adjustment (nm)\n")
    f_before.write("Pore Size (nm)\tProbability Density\n")
    for bin_center, pdf_value in zip(pore_size_distribution_before.bin_centers, pore_size_distribution_before.pdf):
        pore_size_nm = bin_center * pixel_size_nm
        f_before.write(f"{pore_size_nm:.4f}\t{pdf_value:.4f}\n")

    # Calculate average pore size before threshold adjustment
    average_pore_size_pixels_before = np.average(pore_size_distribution_before.bin_centers, weights=pore_size_distribution_before.pdf)
    average_pore_size_nm_before = average_pore_size_pixels_before * pixel_size_nm
    f_before.write(f"\nAverage Pore Size (nm): {average_pore_size_nm_before:.4f}\n")

    # Print the results before threshold adjustment
    print("Pore Size Distribution before threshold adjustment saved to:")
    print(filename_before)

# Save the segmented image
segmented_image_filename = os.path.join(output_subdir, 'segmented_image.png')
skimage.io.imsave(segmented_image_filename, thresholded_image.astype(np.uint8) * 255)

# Calculate the pore size distribution on the segmented image
pore_size_distribution_after = porespy.metrics.pore_size_distribution(thresholded_image)

# Save results after threshold adjustment to file
filename_after = os.path.join(output_subdir, 'pore_size_distribution.txt')
with open(filename_after, 'w') as f_after:
    f_after.write("Pore Size Distribution After Threshold Adjustment (nm)\n")
    f_after.write("Pore Size (nm)\tProbability Density\n")
    for bin_center, pdf_value in zip(pore_size_distribution_after.bin_centers, pore_size_distribution_after.pdf):
        pore_size_nm = bin_center * pixel_size_nm
        f_after.write(f"{pore_size_nm:.4f}\t{pdf_value:.4f}\n")

    # Calculate average pore size after threshold adjustment
    average_pore_size_pixels_after = np.average(pore_size_distribution_after.bin_centers, weights=pore_size_distribution_after.pdf)
    average_pore_size_nm_after = average_pore_size_pixels_after * pixel_size_nm
    f_after.write(f"\nAverage Pore Size (nm): {average_pore_size_nm_after:.4f}\n")

    # Print the results after threshold adjustment
    print("Pore Size Distribution after threshold adjustment saved to:")
    print(filename_after)

# You can also plot the distribution if needed
# plt.plot(pore_size_distribution.bin_centers, pore_size_distribution.pdf)
# plt.xlabel("Pore Size (nm)")
# plt.ylabel("Probability Density")
# plt.title("Pore Size Distribution")
# plt.show()
