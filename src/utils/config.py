from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
TELEGRAM_CHAT_ID = int(os.getenv("TELEGRAM_CHAT_ID"))
INDEED_API_KEY = os.getenv("INDEED_API_KEY")
PROXYCURL_API_KEY = os.getenv("PROXYCURL_API_KEY")
ZIPRECRUITER_API_KEY = os.getenv("ZIPRECRUITER_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
DISCORD_ROLE_ID = int(os.getenv("DISCORD_ROLE_ID"))
TELEGRAM_ADMIN_ID = int(os.getenv("TELEGRAM_ADMIN_ID"))
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
