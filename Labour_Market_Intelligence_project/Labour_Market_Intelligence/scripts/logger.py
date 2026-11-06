import logging

from config import LOG_FILE

# Create logger
logger = logging.getLogger("LabourMarket")

# Avoid duplicate handlers
if not logger.handlers:

    logger.setLevel(logging.INFO)

# File handler
    file_handler = logging.FileHandler(LOG_FILE)

# Console handler
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)