import logging
import sys
from DataManager import config

# Logger configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=config.log_level,
)

logger = logging.getLogger(__name__)

# Set a handler for the INFO level
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(info_handler)

# Set a handler for the ERROR level
error_handler = logging.FileHandler(config.log_file_path, mode='a')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(error_handler)
