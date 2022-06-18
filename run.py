"""Script to mirror my home directory on raspberry pi to usb disk"""

import datetime
import logging
import os

SOURCE = "/home/pi/"
DESTINATION = "/media/pi/1/home/"
EXCLUDE = "Downloads/"

CURRENT_DAY = datetime.datetime.now()
WORKING_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(WORKING_DIR, "log")
LOG_FILE_NAME = os.path.join(WORKING_DIR, "log", f"{CURRENT_DAY.strftime('%Y-%m-%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_NAME, mode="a"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def clone_files() -> None:
    """
    Clone files from home to destination

    """

    # -a equivalent to -rlptgoD, a quick way of saying you want recursion and want to preserve almost everything
    # -u forces rsync to skip any files which exist on the destination or apply changes
    # --partial keeps partially transferred files (if transmission is aborted, you don’t need to start over)
    # --delete also remove deleted filed in destination (like cloning SOURCE)
    # -t, --times preserve modification time
    # -p, --perms preserve permissions
    # -exclude-from=

    logger.info("Started")
    os.popen(f"sudo rsync -autp --partial --delete --exclude='{EXCLUDE}' {SOURCE} {DESTINATION}")
    logger.info("Successfully completed")


if __name__ == "__main__":
    clone_files()
