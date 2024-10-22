# Brain Image Analysis Pipeline

## Overview

This repository contains a comprehensive pipeline for analysing brain images which have had cisterna magna tracer infusions.
The pipeline is designed to process multiple directories containing brain image data.

## Features

- Tracer signal segmentation and quantification
- Brain registration using Brainreg (Brainglobe)
- Tracer signal lookup and region analysis
- Automated processing of multiple directories

## Prerequisites

- Python 3.x
- Required Python packages:
  - numpy
  - pandas
  - scikit-image
  - scipy
  - tqdm
  - [Brainreg (Brainglobe)](https://brainglobe.info/tutorials/tutorial-whole-brain-registration.html)

## File Structure

- `main.py`: The main script that orchestrates the entire analysis pipeline.
- `tracer_segmentation.py`: Contains the `TracerSignalAnalyser` class for segmenting and analyzing tracer signals.
- `brain_registration.py`: Contains the `BrainRegistration` class for registering brain images.
- `signal_lookup.py`: Contains the `ImageAnalyser` class for performing tracer signal lookup and region analysis.
- `structures.csv`: A file containing information about brain structures (should be placed in the same directory as the scripts).

## Usage

1. Ensure all required packages are installed.
2. Place your image files in the appropriate directories.
3. Modify the `parent_dir`, `signal_analysis_img`, and `registration_img` variables in the `main.py` file to match your directory structure and file names.
4. Run the `main.py` script:

## TO DO
- add command line interface to simplify running of the script
