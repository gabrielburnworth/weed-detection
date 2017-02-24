#!/usr/bin/env python
"""Parameters for Plant Detection.

For Plant Detection.
"""
import os
import cv2
import json
try:
    from .CeleryPy import CeleryPy
except:
    from CeleryPy import CeleryPy


class Parameters():
    """Input parameters for Plant Detection."""

    def __init__(self):
        """Set initial attributes and defaults."""
        self.parameters = {'blur': 5, 'morph': 5, 'iterations': 1,
                           'H': [30, 90], 'S': [20, 255], 'V': [20, 255]}
        self.array = None  # default
        self.kernel_type = 'ellipse'
        self.morph_type = 'close'
        self.dir = os.path.dirname(os.path.realpath(__file__))[:-3] + os.sep
        self.input_parameters_file = "plant-detection_inputs.json"
        self.output_text = False
        self.output_json = False
        self.tmp_dir = None
        self.JSON_input_parameters = None
        self.calibration_data = None
        self.ENV_VAR_name = 'PLANT_DETECTION_options'

        # Create dictionaries of morph types
        self.kt = {}  # morph kernel type
        self.kt['ellipse'] = cv2.MORPH_ELLIPSE
        self.kt['rect'] = cv2.MORPH_RECT
        self.kt['cross'] = cv2.MORPH_CROSS
        self.mt = {}  # morph type
        self.mt['close'] = cv2.MORPH_CLOSE
        self.mt['open'] = cv2.MORPH_OPEN
        self.mt['erode'] = 'erode'
        self.mt['dilate'] = 'dilate'

    def save(self):
        """Save input parameters to file."""
        def save(directory):
            with open(directory + self.input_parameters_file, 'w') as f:
                json.dump(self.parameters, f)
        try:
            save(self.dir)
        except IOError:
            self.tmp_dir = "/tmp/"
            save(self.tmp_dir)

    def save_to_env_var(self):
        """Save input parameters to environment variable."""
        self.JSON_input_parameters = CeleryPy().set_user_env(
            self.ENV_VAR_name,
            json.dumps(self.parameters))
        os.environ[self.ENV_VAR_name] = json.dumps(self.parameters)

    def load(self):
        """Load input parameters from file."""
        def load(directory):
            with open(directory + self.input_parameters_file, 'r') as f:
                self.parameters = json.load(f)
        try:
            load(self.dir)
        except IOError:
            self.tmp_dir = "/tmp/"
            load(self.tmp_dir)

    def load_env_var(self):
        """Read input parameters from JSON in environment variable."""
        self.parameters = json.loads(os.environ[self.ENV_VAR_name])

    def load_defaults_for_env_var(self):
        """Load default input parameters for environment variable."""
        self.parameters = {'blur': 15, 'morph': 6, 'iterations': 4,
                           'H': [30, 90], 'S': [50, 255], 'V': [50, 255]}

    def print_input(self):
        """Print input parameters."""
        print('Processing Parameters:')
        print('-' * 25)
        print('Blur kernel size: {}'.format(self.parameters['blur']))
        print('Morph kernel size: {}'.format(self.parameters['morph']))
        print('Iterations: {}'.format(self.parameters['iterations']))
        print('Hue:\n\tMIN: {}\n\tMAX: {}'.format(*self.parameters['H']))
        print('Saturation:\n\tMIN: {}\n\tMAX: {}'.format(
            *self.parameters['S']))
        print('Value:\n\tMIN: {}\n\tMAX: {}'.format(*self.parameters['V']))
        print('-' * 25)

if __name__ == "__main__":
    parameters = Parameters()
    try:
        parameters.load()
    except IOError:
        print("No parameters file.")
    parameters.print_input()
    parameters.parameters['iterations'] = 4
    parameters.print_input()
    parameters.save()
