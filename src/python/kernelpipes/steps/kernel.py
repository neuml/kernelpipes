"""
Kernel module
"""

import logging
import os

import kaggle

from .step import Step

class Kernel(Step):
    """
    Step to execute a Kaggle Kernel.
    """

    def __init__(self, directory, kernel):
        """
        Creates a new Kernel step.

        Args:
            directory: pipeline working directory
            kernel: kernel name
        """

        self.directory = directory
        self.kernel = kernel

    def run(self):
        """
        Executes a Kaggle Kernel.
        """

        logging.info("Running Kernel: %s", self.kernel)

        path = os.path.join(self.directory, self.kernel)

        # Pull down latest version of kernel
        kaggle.api.kernels_pull(self.kernel, path, True, False)

        # Push and run the kernel
        kaggle.api.kernels_push(path)
