from apify_client import ApifyClient
from src.utils.config import APIFY_API_TOKEN
from src.utils.logger import setup_logger

logger = setup_logger()

def get_apify_client():
 try:
 client = ApifyClient(APIFY_API_TOKEN)
 logger.info("Initialized Apify client")
 return client
 except Exception as e:
 logger.error(f"Failed to initialize Apify client: {e}")
 return None
