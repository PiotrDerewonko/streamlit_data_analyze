import logging
import os
from dotenv import load_dotenv

def get_logger(name='app'):
    load_dotenv()
    level = os.getenv('LOG_LEVEL', 'logging.INFO')
    filemode = os.getenv('LOG_FILEMODE', 'a')
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Uniknij duplikowania handlerów
    if logger.hasHandlers():
        return logger

    # Upewnij się, że katalog logów istnieje
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Ścieżka do pliku logu
    log_path = os.path.abspath(os.path.join(log_dir, f'{name}.log'))

    # Tworzymy FileHandler
    file_handler = logging.FileHandler(log_path, mode=filemode)
    file_handler.setLevel(level)

    # Format logów
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Dodajemy handler do loggera
    logger.addHandler(file_handler)

    return logger
