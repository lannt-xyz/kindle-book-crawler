import logging
from logging.handlers import RotatingFileHandler

# Create a rotating file handler
log_file = '/var/logs/kindle-book-crawer.log'
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")  # 5 MB per file, keep 3 backups
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Get the logger and set the level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add the rotating file handler to the logger
logger.addHandler(handler)

# Optionally, add a console handler if you want to see logs in the console as well
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
