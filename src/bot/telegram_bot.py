from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from src.utils.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ADMIN_ID
from src.utils.logger import setup_logger
from src.utils.database import JobDatabase
from src.utils.formatter import format_telegram_message
from src.api.indeed import scrape_indeed_jobs
from src.api.linkedin import scrape_linkedin_jobs
from src.api.ziprecruiter import scrape_ziprecruiter_jobs
from src.api.glassdoor import scrape_glassdoor_jobs
from src.api.monster import scrape_monster_jobs
from src.api.cryptojobslist import scrape_cryptojobslist_jobs

logger = setup_logger()

class CyberJobBot:
 def __init__(self):
 self.db = JobDatabase()
 self.filters = {"location": None, "salary": None, "experience": None}
 
 async def post_jobs(self, context: ContextTypes.DEFAULT_TYPE):
 logger.info("Starting Telegram post_jobs")
 chat_id = TELEGRAM_CHAT_ID
 
 try:
 jobs = []
 for platform, scrape_func in [
 ("Indeed", scrape_indeed_jobs),
 ("LinkedIn", scrape_linkedin_jobs),
 ("ZipRecruiter", scrape_ziprecruiter_jobs),
 ("Glassdoor", scrape_glassdoor_jobs),
 ("Monster", scrape_monster_jobs),
 ("CryptoJobsList", scrape_cryptojobslist_jobs)
 ]:
 try:
 platform_jobs = scrape_func()
 logger.info(f"Scraped {len(platform_jobs)} jobs from {platform}")
 jobs.extend(platform_jobs)
 except Exception as e:
 logger.error(f"Failed to scrape {platform}: {e}")
 
 if not jobs:
 logger.warning("No jobs scraped from any platform")
 return
 
 for job in jobs:
 if self.filters.get("location") and self.filters["location"].lower() not in job["location"].lower():
 continue
 if self.filters.get("salary") and job["salary"] != "N/A" and self.filters["salary"] not in job["salary"]:
 continue
 if self.filters.get("experience") and job["requirements"] != "N/A" and self.filters["experience"].lower() not in job["requirements"].lower():
 continue
 
 if not self.db.job_exists(job["id"]):
 message = format_telegram_message(job)
 if message:
 logger.info(f"Sending job to Telegram: {job['title']}")
 await context.bot.send_message(
 chat_id=chat_id,
 text=f"@{TELEGRAM_ADMIN_ID} New job posted!\n{message}",
 parse_mode="Markdown"
 )
 self.db.add_job(
 job["id"], job["title"], job["company"], job["location"],
 job["salary"], job["requirements"], job["url"], job["platform"]
 )
 logger.info(f"Posted job to Telegram: {job['title']}")
 else:
 logger.info(f"Skipping duplicate job: {job['title']}")
 except Exception as e:
 logger.error(f"Error in Telegram post_jobs: {e}", exc_info=True)
 
 async def refresh(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text("🔄 Fetching new cybersecurity jobs... Please wait!")
 try:
 await self.post_jobs(context)
 await update.message.reply_text("✅ Job refresh complete! Check the channel for new postings. 🚀")
 except Exception as e:
 await update.message.reply_text("❌ Error refreshing jobs. Check logs.")
 logger.error (f"Error in refresh command: {e}", exc_info=True)
 
 async def filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
 if len(context.args) < 2:
 await update.message.reply_text("Usage: /filter <type> <value> (e.g., /filter location London)")
 return
 filter_type, value = context.args[0], " ".join(context.args[1:])
 if filter_type.lower() not in ["location", "salary", "experience"]:
 await update.message.reply_text("Invalid filter type. Use: location, salary, experience")
 return
 self.filters[filter_type.lower()] = value
 await update.message.reply_text(f"Set filter {filter_type} to: {value}")
 logger.info(f"Set Telegram filter {filter_type} to {value}")
 
 async def clear_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
 self.filters = {"location": None, "salary": None, "experience": None}
 await update.message.reply_text("Cleared all filters")
 logger.info("Cleared all Telegram filters")
 
 async def list_jobs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
 platform = context.args[0] if context.args else None
 jobs = self.db.query_jobs(platform=platform)
 if not jobs:
 await update.message.reply_text("No jobs found")
 return
 for job in jobs[:5]:
 message = format_telegram_message({
 "id": job[0], "title": job[1], "company": job[2], "location": job[3],
 "salary": job[4], "requirements": job[5], "url": job[6], "platform": job[7],
 "posted_at": job[8]
 })
 if message:
 await update.message.reply_text(message, parse_mode="Markdown")
 await update.message.reply_text(f"Displayed {min(len(jobs), 5)} of {len(jobs)} jobs")

def run_telegram_bot():
 try:
 bot = CyberJobBot()
 application = Application.builder().token(TELEGRAM_TOKEN).build()
 
 application.add_handler(CommandHandler("refresh", bot.refresh))
 application.add_handler(CommandHandler("filter", bot.filter))
 application.add_handler(CommandHandler("clear_filters", bot.clear_filters))
 application.add_handler(CommandHandler("list_jobs", bot.list_jobs))
 
 application.job_queue.run_repeating(bot.post_jobs, interval=3600, first=10)
 application.run_polling()
 except Exception as e:
 logger.error(f"Telegram bot crashed: {e}", exc_info=True)
