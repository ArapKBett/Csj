from src.bot.discord_bot import run_discord_bot
from src.bot.telegram_bot import run_telegram_bot
from src.web.app import run_flask_app
import threading
from src.utils.logger import setup_logger

logger = setup_logger()

def main():
 logger.info("Starting Cybersecurity Job Bot...")
 
 discord_thread = threading.Thread(target=run_discord_bot, daemon=True, name="DiscordBot")
 telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True, name="TelegramBot")
 flask_thread = threading.Thread(target=run_flask_app, daemon=True, name="FlaskApp")
 
 discord_thread.start()
 telegram_thread.start()
 flask_thread.start()
 
 try:
 while True:
 if not discord_thread.is_alive():
 logger.error("Discord thread stopped unexpectedly")
 discord_thread = threading.Thread(target=run_discord_bot, daemon=True, name="DiscordBot")
 discord_thread.start()
 if not telegram_thread.is_alive():
 logger.error("Telegram thread stopped unexpectedly")
 telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True, name="TelegramBot")
 telegram_thread.start()
 if not flask_thread.is_alive():
 logger.error("Flask thread stopped unexpectedly")
 flask_thread = threading.Thread(target=run_flask_app, daemon=True, name="FlaskApp")
 flask_thread.start()
 threading.Event().wait(60)
 except KeyboardInterrupt:
 logger.info("Shutting down bots...")
 exit(0)
 except Exception as e:
 logger.error(f"Main thread error: {e}", exc_info=True)

if __name__ == "__main__":
 main()
