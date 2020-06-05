"""
Step module
"""

import time

class Step(object):
    """
    Base Step class. All steps inherit from this class.
    """

    def __call__(self):
        """
        Executes a step.

        Returns:
            run results
        """

        return self.run()

    def run(self):
        """
        Executes a Step.

        Returns:
            run results
        """

        return None

    def wait(self, duration):
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
