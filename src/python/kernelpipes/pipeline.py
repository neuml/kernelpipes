"""
Pipeline module
"""

import os
import sys
import time

import kaggle
import yaml

class Pipeline(object):
    """
    Kaggle Kernel Pipeline execution methods using the Kaggle API.
    """

    @staticmethod
    def wait(duration):
        """
        Sleeps for the duration passed in. Supports suffixed strings (minutes, seconds, hours)
        """

        # Convert string to number of seconds as a float
        if isinstance(duration, str):
            if duration.endswith("s"):
                duration = float(duration.rstrip("s").strip())
            elif duration.endswith("m"):
                duration = float(duration.rstrip("m").strip()) * 60
            elif duration.endswith("h"):
                duration = float(duration.rstrip("h").strip()) * 60 * 60
            else:
                duration = float(duration)

        # Wait duration seconds
        time.sleep(max(duration, 1))

    @staticmethod
    def status(kernels, wait):
        """
        Waits for completion of the input kernels.

        Args:
            kernels: list of kernels to check status for
            wait: wait duration between status checks

        Returns:
            list of (kernel, status, message)
        """

        results = []

        while kernels:
            for kernel in kernels:
                # Check status of the job
                result = kaggle.api.kernels_status(kernel)
                status, message = result["status"], result["failureMessage"]

                # Save status if completed
                if status not in ("running", "queued"):
                    results.append((kernel, status, message))

            # Remove completed jobs
            for kernel, _, _ in results:
                if kernel in kernels:
                    kernels.remove(kernel)

            # Wait for the specified duration
            print("Waiting for %s" % wait)
            Pipeline.wait(wait)

        return results

    @staticmethod
    def kernel(directory, kernel):
        """
        Executes a Kaggle Kernel.

        Args:
            directory: pipeline working directory
            kernel: kernel name
        """

        path = os.path.join(directory, kernel)

        # Pull down latest version of kernel
        kaggle.api.kernels_pull(kernel, path, True, False)

        # Push and run the kernel
        kaggle.api.kernels_push(path)

    @staticmethod
    def run(task):
        """
        Executes a kernel pipeline.

        Args:
            task: path to pipeline task YAML file
        """

        # Load pipeline YAML file
        with open(task, "r") as f:
            # Read configuration
            pipeline = yaml.safe_load(f)

        # Initialize variables
        directory, kernels, errors = os.path.dirname(task), [], False

        print("Executing pipeline:", pipeline["name"])
        for step in pipeline["steps"]:
            if "kernel" in step:
                print("Running Kernel: ", step["kernel"])
                Pipeline.kernel(directory, step["kernel"])
                kernels.append(step["kernel"])

            elif "status" in step:
                # Waiting for completion of all running jobs
                for kernel, status, message in Pipeline.status(kernels, step["status"]):
                    # Check for errors and return if found
                    if status != "complete" or message:
                        print("ERROR:", kernel, status, message)
                    else:
                        print("Kernel Complete:", kernel)

                # If any errors found, break out of processing loop
                if errors:
                    return

                # Reset kernels
                kernels = []

        print("Pipeline complete")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        Pipeline.run(sys.argv[1])
    else:
        print("Usage: pipeline <path to pipeline.yml file>")
