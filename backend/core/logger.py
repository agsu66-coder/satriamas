"""
TERATAI Logger
"""

from datetime import datetime


class Logger:

    def info(self, message):

        print(
            f"[INFO] "
            f"{datetime.now():%H:%M:%S} "
            f"{message}"
        )

    def warning(self, message):

        print(
            f"[WARNING] "
            f"{datetime.now():%H:%M:%S} "
            f"{message}"
        )

    def error(self, message):

        print(
            f"[ERROR] "
            f"{datetime.now():%H:%M:%S} "
            f"{message}"
        )


logger = Logger()