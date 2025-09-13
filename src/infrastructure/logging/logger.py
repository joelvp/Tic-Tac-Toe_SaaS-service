import logging
import sys

logger = logging.getLogger("tic_tac_toe")
logger.setLevel(logging.INFO)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
stderr_handler.setFormatter(formatter)

logger.addHandler(stderr_handler)
