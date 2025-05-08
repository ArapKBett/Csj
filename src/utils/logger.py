import logging
import os

def setup_logger():
 logger = logging.getLogger("CyberJobBot")
 logger.setLevel(logging.INFO)
 
 if not os.path.exists("logs"):
 os.makedirs("logs")
 
 file_handler = logging.FileHandler("logs/bot.log")
 file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
 logger.addHandler(file_handler)
 
 return logger
