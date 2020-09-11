# import logging
# from pathlib import Path

# # setup loggers
# LOGGING_CONFIG = Path(__file__).parent / "logging.conf"
# logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)

# logger = logging.getLogger(__name__)
# breakpoint()

import logging

logging.root.handlers = []
logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s",
    level=logging.INFO,
    filename="logs/app.log",
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
# set a format which is simpler for console use
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)
