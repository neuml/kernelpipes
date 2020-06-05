"""
Status module
"""

import logging

import kaggle

from .step import Step

class Status(Step):
    """
    Step to check the status for a list of Kaggle Kernels.
    """

    def __init__(self, kernels, duration):
        """
        Creates a Status step.

        Args:
            kernels: list of kernels to check status for
            duration: wait duration between status checks
        """

        self.kernels = kernels
        self.duration = duration

    def run(self):
        """
        Waits for completion of the input kernels.

        Returns:
            list of (kernel, status, message)
        """

        results = []
        errors = False

        while self.kernels:
            for kernel in self.kernels:
                # Check status of the job
                result = kaggle.api.kernels_status(kernel)
                status, message = result["status"], result["failureMessage"]

                # Save status if completed
                if status not in ("running", "queued"):
                    results.append((kernel, status, message))

            # Remove completed jobs
            for kernel, _, _ in results:
                if kernel in self.kernels:
                    self.kernels.remove(kernel)

            # Wait for the specified duration
            logging.info("Waiting for %s", self.duration)
            self.wait(self.duration)

        # Waiting for completion of all running jobs
        for kernel, status, message in results:
            # Check for errors and return if found
            if status != "complete" or message:
                logging.error("ERROR: %s %s %s", kernel, status, message)
                errors = True
            else:
                logging.info("Kernel Complete: %s", kernel)

        # Return true if all kernels completed successfully
        return not errors
