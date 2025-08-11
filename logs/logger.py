# Logger writen by ChatGPT cuz I couldn't be assed to do it myself
import logging
import os

def get_logger(name: str = "app_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Make sure logs/ directory exists
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", "logs.log")

        fh = logging.FileHandler(log_path, mode="a")
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        fh.setFormatter(formatter)

        logger.addHandler(fh)
    return logger

default_logger = get_logger()


