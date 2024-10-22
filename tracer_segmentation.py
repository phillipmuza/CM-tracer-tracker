# Title: Segment tracer from brains, and quantify tracer coverage
# Author: Phillip Muza
# Date:  21.08.24

import os, numpy as np, pandas as pd
from skimage.filters import median, gaussian, threshold_yen, threshold_triangle
from skimage.io import imread, imsave
from skimage.util import img_as_uint, img_as_float
from tqdm import tqdm


class TracerSignalAnalyser:
    def __init__(self, image_stack):
        """
        Initialize the TracerSignalAnalyzer with the given image stack.

        Parameters:
        image_stack (numpy.ndarray): 3D image stack containing the fluorescent signal.
        """
        if not isinstance(image_stack, np.ndarray) or image_stack.ndim != 3:
            raise ValueError("Image stack must be a 3D numpy array")
        self.image_stack = image_stack
        self.median_filtered = None
        self.gaussian_blurred = None
        self.sharp_img = None
        self.results = None

    def median_filtering(self):
        """
        Apply a 3D median filter to the image stack.
        """
        print("Applying 3D median filter...")
        footprint = np.ones((3, 3, 3), dtype=bool)
        self.median_filtered = median(self.image_stack, footprint=footprint)

    def apply_image_mask(self):
        """
        Apply a mask to remove background artifacts.
        """
        print("Applying image mask to remove background artifacts...")
        img_mask = np.zeros_like(self.median_filtered, dtype="uint8")
        for i in tqdm(range(self.median_filtered.shape[2]), desc="Masking slices"):
            thresh = threshold_triangle(self.median_filtered[:, :, i])
            img_mask[:, :, i] = (self.median_filtered[:, :, i] > (thresh * 1.7)).astype(int)
        imsave("image_mask.tif", img_mask)
        self.median_filtered *= img_mask
        
    def gaussian_blur(self):
        """
        Apply Gaussian blur to the median-filtered image stack.
        """
        print("Applying Gaussian blur...")
        median_filtered_float = img_as_float(self.median_filtered)
        self.gaussian_blurred = img_as_uint(gaussian(median_filtered_float, sigma=(20, 20, 20), preserve_range=True))

    def unsharp_masking(self):
        """
        Perform unsharp masking by subtracting the Gaussian-blurred image from the median-filtered image.
        """
        print("Performing unsharp masking...")
        self.sharp_img = np.maximum(self.median_filtered.astype(np.int16) - self.gaussian_blurred.astype(np.int16), 0)
        imsave("unsharp_image.tif", self.sharp_img)

    def measure_area(self):
        """
        Measure the percentage area of the tracer signal in each slice using the Yen threshold, and save thresholded image
        """
        print("Measuring the percentage area of the tracer signal...")
        data = {'slice': [], 'percentage_area': []}
        thresholded_image = np.zeros_like(self.sharp_img, dtype="uint8")

        for i in tqdm(range(self.sharp_img.shape[2]), desc="Measuring slices"):
            thresh = threshold_yen(self.sharp_img[:, :, i])
            binary_slice = self.sharp_img[:, :, i] > thresh
            signal_area = np.sum(binary_slice)
            total_area = binary_slice.size
            percentage_area = (signal_area / total_area) * 100
            data['slice'].append(i + 1)
            data['percentage_area'].append(percentage_area)
        
            # Create the thresholded image
            thresholded_image[:, :, i] = (binary_slice).astype(np.uint8)
        
        self.results = pd.DataFrame(data)
        imsave("thresholded_image.tif", thresholded_image)

    def save_results(self, filename="tracer_percentage_area.csv"):
        """
        Save the results to a CSV file.

        Parameters:
        filename (str): Name of the CSV file to save the results.
        """
        print(f"Saving results to {filename}...")
        self.results.to_csv(filename, index=False)

    def process(self):
        """
        Run the complete analysis process.
        """
        self.median_filtering()
        self.apply_image_mask()
        self.gaussian_blur()
        self.unsharp_masking()
        self.measure_area()
        self.save_results()

os.chdir("Y:\\python_analysis\\an11")

# Example usage:
# image_stack = imread("<your 3D numpy array>")
# analyser = TracerSignalAnalyser(image_stack)
# results = analyser.process()
# analyser.save_results()