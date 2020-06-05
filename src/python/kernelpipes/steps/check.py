"""
Check module
"""

import json
import logging
import os

import kaggle

from .step import Step

class Check(Step):
    """
    Step to check if a Kaggle dataset has been updated since the last run.
    """

    def __init__(self, directory, dataset):
        """
        Creates a dataset status check step.

        Args:
            directory: pipeline working directory
            dataset: dataset name
        """

        self.directory = directory
        self.dataset = dataset

    def run(self):
        """
        Determines if the dataset has been updated since the last run.
        """

        logging.info("Querying dataset %s for updates", self.dataset)

        # Attempt to load previous metadata
        path = os.path.join(self.directory, self.dataset, "metadata.json")
        if os.path.exists(path):
            with open(path) as f:
                metadata = json.load(f)
        else:
            metadata = None

        # Pull down latest dataset metadata and number of files
        latest = kaggle.api.dataset_view(self.dataset)
        files = len(kaggle.api.dataset_list_files(self.dataset).files)

        # Get current metadata fields
        version, updated = getattr(latest, "currentVersionNumber"), getattr(latest, "lastUpdated").isoformat()

        # Check updates returns true if there is no local metadata file or
        # the latest version is newer than the stored version
        if not metadata or (version > int(metadata["version"]) and files):
            # Create parent directory
            os.makedirs(os.path.dirname(path), exist_ok=True)

            with open(path, "w") as f:
                json.dump({"version": version, "date": updated}, f)

            if metadata:
                logging.info("%s new version %d (%s) found - prior version %d (%s)",
                             self.dataset, version, updated, metadata["version"], metadata["date"])
            else:
                logging.info("%s has no local metadata, proceeding with run", self.dataset)

            return True

        logging.info("%s up-to-date", self.dataset)
        return False
