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
thresholded_image = image > thresh

# Save the segmented image
segmented_image_filename = os.path.join(output_subdir, 'segmented_image.png')
skimage.io.imsave(segmented_image_filename, thresholded_image.astype(np.uint8) * 255)

# Calculate the pore size distribution on the segmented image
pore_size_distribution = porespy.metrics.pore_size_distribution(thresholded_image)

# Save results to file
filename = os.path.join(output_subdir, 'pore_size_distribution.txt')
with open(filename, 'w') as f:
    f.write("Pore Size Distribution (nm)\n")
    f.write("Pore Size (nm)\tProbability Density\n")
    for bin_center, pdf_value in zip(pore_size_distribution.bin_centers, pore_size_distribution.pdf):
        pore_size_nm = bin_center * pixel_size_nm
        f.write(f"{pore_size_nm:.4f}\t{pdf_value:.4f}\n")

    # Calculate average pore size
    average_pore_size_pixels = np.average(pore_size_distribution.bin_centers, weights=pore_size_distribution.pdf)
    average_pore_size_nm = average_pore_size_pixels * pixel_size_nm
    f.write(f"\nAverage Pore Size (nm): {average_pore_size_nm:.4f}\n")

    # Print the results
    print("Pore Size Distribution saved to:")
    print(filename)

# You can also plot the distribution if needed
# plt.plot(pore_size_distribution.bin_centers, pore_size_distribution.pdf)
# plt.xlabel("Pore Size (nm)")
# plt.ylabel("Probability Density")
# plt.title("Pore Size Distribution")
# plt.show()
