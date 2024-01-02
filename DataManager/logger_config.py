import logging
import sys
from DataManager import config

# Configurazione del logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=config.log_level,  # Imposta su DEBUG in modo da includere tutti i livelli di log
)

# Crea un logger
logger = logging.getLogger(__name__)

# Imposta un gestore per il livello INFO
info_handler = logging.StreamHandler(sys.stdout)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(info_handler)

# Imposta un gestore per il livello ERROR
error_handler = logging.FileHandler(config.log_file_path, mode='a')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(error_handler)
