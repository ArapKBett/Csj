import discord
from discord.ext import commands, tasks
from src.utils.config import DISCORD_TOKEN, DISCORD_CHANNEL_ID, DISCORD_ROLE_ID
from src.utils.logger import setup_logger
from src.utils.database import JobDatabase
from src.utils.formatter import format_discord_embed
from src.api.indeed import scrape_indeed_jobs
from src.api.linkedin import scrape_linkedin_jobs
from src.api.ziprecruiter import scrape_ziprecruiter_jobs
from src.api.glassdoor import scrape_glassdoor_jobs
from src.api.monster import scrape_monster_jobs
from src.api.cryptojobslist import scrape_cryptojobslist_jobs

logger = setup_logger()

class CyberJobBot(commands.Bot):
 def __init__(self):
 intents = discord.Intents.default()
 intents.message_content = True
 super().__init__(command_prefix="/", intents=intents)
 self.db = JobDatabase()
 self.filters = {"location": None, "salary": None, "experience": None}
 
 async def setup_hook(self):
 logger.info("Starting Discord job posting task")
 try:
 self.post_jobs.start()
 logger.info("Discord post_jobs task started")
 await self.post_jobs()
 logger.info("Initial Discord post_jobs run completed")
 except Exception as e:
 logger.error(f"Error in setup_hook: {e}", exc_info=True)
 
 async def on_ready(self):
 logger.info(f"Discord bot {self.user} is ready!")
 logger.info(f"Connected to guilds: {[guild.name for guild in self.guilds]}")
 channel = self.get_channel(DISCORD_CHANNEL_ID)
 logger.info(f"Channel {DISCORD_CHANNEL_ID} found: {channel}")
 if channel:
 permissions = channel.permissions_for(channel.guild.me)
 logger.info(f"Bot permissions in channel {DISCORD_CHANNEL_ID}: {permissions}")
 logger.info(f"Send Messages: {permissions.send_messages}, Embed Links: {permissions.embed_links}")
 if not permissions.send_messages or not permissions.embed_links:
 logger.error("Bot lacks Send Messages or Embed Links permissions")
 
 @tasks.loop(hours=1)
 async def post_jobs(self):
 logger.info("Starting Discord post_jobs")
 channel = self.get_channel(DISCORD_CHANNEL_ID)
 if not channel:
 logger.error("Discord channel not found!")
 return
 
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
 embed = format_discord_embed(job)
 if embed:
 logger.info(f"Sending job to Discord: {job['title']}")
 await channel.send(content=f"<@&{DISCORD_ROLE_ID}> New job posted!", embed=embed)
 self.db.add_job(
 job["id"], job["title"], job["company"], job["location"],
 job["salary"], job["requirements"], job["url"], job["platform"]
 )
 logger.info(f"Posted job to Discord: {job['title']}")
 else:
 logger.info(f"Skipping duplicate job: {job['title']}")
 except Exception as e:
 logger.error(f"Error in Discord post_jobs: {e}", exc_info=True)
 
 @commands.command()
 async def refresh(self, ctx):
 await ctx.send("🔄 Fetching new cybersecurity jobs... Please wait!")
 try:
 await self.post_jobs()
 await ctx.send("✅ Job refresh complete! Check the channel for new postings. 🚀")
 except Exception as e:
 await ctx.send("❌ Error refreshing jobs. Check logs.")
 logger.error(f"Error in refresh command: {e}", exc_info=True)
 
 @commands.command()
 async def filter(self, ctx, filter_type, *, value):
 if filter_type.lower() not in ["location", "salary", "experience"]:
 await ctx.send("Invalid filter type. Use: location, salary, experience")
 return
 self.filters[filter_type.lower()] = value
 await ctx.send(f"Set filter {filter_type} to: {value}")
 logger.info(f"Set Discord filter {filter_type} to {value}")
 
 @commands.command()
 async def clear_filters(self, ctx):
 self.filters = {"location": None, "salary": None, "experience": None}
 await ctx.send("Cleared all filters")
 logger.info("Cleared all Discord filters")
 
 @commands.command()
 async def list_jobs(self, ctx, platform=None):
 jobs = self.db.query_jobs(platform=platform)
 if not jobs:
 await ctx.send("No jobs found")
 return
 for job in jobs[:5]:
 embed = format_discord_embed({
 "id": job[0], "title": job[1], "company": job[2], "location": job[3],
 "salary": job[4], "requirements": job[5], "url": job[6], "platform": job[7],
 "posted_at": job[8]
 })
 if embed:
 await ctx.send(embed=embed)
 await ctx.send(f"Displayed {min(len(jobs), 5)} of {len(jobs)} jobs")

def run_discord_bot():
 try:
 bot = CyberJobBot()
 bot.run(DISCORD_TOKEN, reconnect=True)
 except Exception as e:
 logger.error(f"Discord bot crashed: {e}", exc_info=True)
