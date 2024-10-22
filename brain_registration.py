# Title: Brain registration using Brainreg (Brainglobe)
# Author: Phillip Muza
# Date:  22.08.24

import subprocess
import os

class BrainRegistration:
    def __init__(self, input_file, output_dir, voxel_size="25 25 25", orientation="asr"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.voxel_size = voxel_size
        self.orientation = orientation
        
    def create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
        else:
            print(f"Output directory already exists: {self.output_dir}")
        
    def generate_command(self):
        return f"brainreg {self.input_file} {self.output_dir} -v {self.voxel_size} --orientation {self.orientation}"
    
    def run_registration(self):
        self.create_output_dir()
        command = self.generate_command()
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            print("Brain registration completed successfully.")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during brain registration: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

# Example usage:
#registrator = BrainRegistration(input_file=r"Y:\trial_analysis\registration.tif", output_dir="registration")
#registrator.run_registration()