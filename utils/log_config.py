import logging
import sys

logging.basicConfig(
    stream=sys.stdout,        # logs go to stdout
    level=logging.INFO,       # change to DEBUG if we want debug logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def get_logger(name=None):
    return logging.getLogger(name)
