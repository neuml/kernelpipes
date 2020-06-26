"""
Output module
"""

import logging

import kaggle

from .step import Step

class Output(Step):
    """
    Step to retrieve Kaggle Kernel Output.
    """

    def __init__(self, directory, kernel):
        """
        Creates a new Output step.

        Args:
            directory: pipeline working directory
            kernel: kernel name
        """

        self.directory = directory
        self.kernel = kernel

    def run(self):
        """
        Retrieves Kaggle Kernel Output.
        """

        logging.info("Retrieving output files for Kernel: %s", self.kernel)

        # Retrieve output
        kaggle.api.kernels_output(self.kernel, self.directory)
