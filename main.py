# Title: Main Analysis Script to run Tracer Segmentation, Brain Registration and Signal Lookup
# Author: Phillip Muza
# Date: 23.08.24

import os
from tracer_segmentation import TracerSignalAnalyser
from brain_registration import BrainRegistration
from signal_lookup import ImageAnalyser
from tqdm import tqdm
from skimage.io import imread
import logging
import time


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_directory(base_dir, signal_analysis_img, registration_img, path_to_structures_file):
    logger = logging.getLogger(__name__)

    logger.info(f"Starting analysis in directory: {base_dir}")
    os.chdir(base_dir)

    steps = ["Tracer Segmentation", "Brain Registration", "Signal Lookup"]
    
    for step in tqdm(steps, desc="Overall Progress"):
        if step == "Tracer Segmentation":
            logger.info("Starting Tracer Segmentation")
            start_time = time.time()
            image_stack = imread(signal_analysis_img) 
            tracer_analyser = TracerSignalAnalyser(image_stack)
            tracer_analyser.process()
            logger.info(f"Tracer Segmentation completed in {time.time() - start_time:.2f} seconds")

        elif step == "Brain Registration":
            logger.info("Starting Brain Registration")
            start_time = time.time()
            registrator = BrainRegistration(input_file=registration_img, output_dir="registration_dir")
            registrator.run_registration()
            logger.info(f"Brain Registration completed in {time.time() - start_time:.2f} seconds")

        elif step == "Signal Lookup":
            logger.info("Starting Signal Lookup")
            start_time = time.time()
            analyser = ImageAnalyser(base_dir)
            analyser.run_analysis(
                "thresholded_image.tif",
                "registration_dir/registered_atlas.tiff", 
                path_to_structures_file,
                "registration_dir/volumes.csv"
            )
            logger.info(f"Machine Learning Lookup completed in {time.time() - start_time:.2f} seconds")

    logger.info("Analysis complete. Results are saved in the respective output files.")
    logger.info("Final decoded results are in the 'decoded_df' attribute of the ImageAnalyser instance.")

def main(parent_dir, signal_analysis_img, registration_img):
    setup_logging()
    logger = logging.getLogger(__name__)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the path to structures file relative to the script location
    path_to_structures_file = os.path.join(script_dir, "structures.csv")

    # Walk through all subdirectories
    for root, dirs, files in os.walk(parent_dir):
        if "decoded_region_counts.csv" in files:
            print(f"Already processed files in {os.getcwd()}")
            continue
        else:
            if signal_analysis_img in files and registration_img in files:
                logger.info(f"Processing directory: {root}")
                process_directory(root, signal_analysis_img, registration_img, path_to_structures_file)

if __name__ == "__main__":
    # Change your parent directory here
    parent_dir = "Y:/trial_analysis" 
    # Give the name of the image you want to segment the tracer
    signal_analysis_img = "signal_analysis.tif"
    # Give the name of the image you want to register to a reference atlas
    registration_img = "registration.tif"

    main(parent_dir, signal_analysis_img, registration_img)


