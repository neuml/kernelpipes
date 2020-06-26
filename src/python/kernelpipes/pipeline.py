"""
Pipeline module
"""

import logging
import os
import sys
import time

from datetime import datetime

import yaml

from croniter import croniter

from .steps.check import Check
from .steps.kernel import Kernel
from .steps.output import Output
from .steps.status import Status

class Pipeline(object):
    """
    Kaggle Kernel Pipeline execution methods using the Kaggle API.
    """

    @staticmethod
    def execute(directory, pipeline):
        """
        Executes a single pipeline run.

        Args:
            directory: pipeline configuration directory
            pipeline: pipeline configuration
        """

        # List of kernels currently running
        kernels = []

        logging.info("Executing pipeline: %s", pipeline["name"])
        for step in pipeline["steps"]:
            if "check" in step:
                if not Check(directory, step["check"])():
                    break

            elif "kernel" in step:
                Kernel(directory, step["kernel"])()
                kernels.append(step["kernel"])

            elif "output" in step:
                Output(directory, step["output"])()

            elif "status" in step:
                # Break out of processing loop if errors found
                if not Status(kernels, step["status"])():
                    return

                # Reset kernels
                kernels = []

        logging.info("Pipeline complete")

    @staticmethod
    def schedule(directory, pipeline):
        """
        Runs a pipeline job through a job scheduler.

        Args:
            directory: pipeline configuration directory
            pipeline: pipeline configuration
        """

        logging.info("Pipeline scheduler enabled for %s using schedule %s", pipeline["name"], pipeline["schedule"])

        while True:
            # Schedule using localtime
            schedule = croniter(pipeline["schedule"], datetime.now().astimezone()).get_next(datetime)
            logging.info("Next run scheduled for %s", schedule.isoformat())
            time.sleep(schedule.timestamp() - time.time())

            Pipeline.execute(directory, pipeline)

    @staticmethod
    def run(task):
        """
        Executes a kernel pipeline loop.

        Args:
            task: path to pipeline task YAML file
        """

        # Initialize logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(module)-10s: %(message)s")

        # Load pipeline YAML file
        with open(task, "r") as f:
            # Read configuration
            pipeline = yaml.safe_load(f)

        if "name" not in pipeline or "steps" not in pipeline:
            logging.error("Pipeline name and steps fields are required")
            return

        # Get base directory where pipeline configuration stored
        directory = os.path.dirname(task)

        # Check if pipeline should be schedule or run a single time
        if "schedule" in pipeline:
            # Job scheduler
            Pipeline.schedule(directory, pipeline)
        else:
            # Single run
            Pipeline.execute(directory, pipeline)

def main():
    """
    Main execution loop.
    """

    if len(sys.argv) > 1:
        Pipeline.run(sys.argv[1])
    else:
        print("Usage: pipeline <path to pipeline.yml file>")

if __name__ == "__main__":
    main()
