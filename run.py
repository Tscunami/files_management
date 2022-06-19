
"""Script to mirror my home directory on raspberry pi to usb disk"""

import datetime
import logging
import os

SOURCE = "/"
DESTINATION = "/media/pi/1/backup/"
EXCLUDE = "/home/pi/Downloads/"

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
    # -o preserve same owner
    # -g preserve same group
    # -exclude-from=

    logger.info("Started")
    
    # Backup crontab file
    os.popopen("crontab -l > /home/pi/cron_scripts/cronjobs") 
    
    # Backup HOME folder without Downloads
    HOME = "home/pi/"
    os.popen(f"sudo rsync -autogp --partial --delete --exclude='{EXCLUDE}' {SOURCE}{HOME} {DESTINATION}{HOME}")
    
    # Backup /etc/update-motd.d folder
    MOTD = "etc/update-motd.d/"
    os.popen(f"sudo rsync -autogp --partial --delete {SOURCE}{MOTD} {DESTINATION}{MOTD}")
    logger.info("Successfully completed")


if __name__ == "__main__":
    clone_files()
