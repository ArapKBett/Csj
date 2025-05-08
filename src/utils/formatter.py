import discord
from src.utils.logger import setup_logger

logger = setup_logger()

def format_discord_embed(job):
 try:
 embed = discord.Embed(title=job["title"], url=job["url"], color=0x00ff00)
 embed.add_field(name="Company", value=job["company"], inline=True)
 embed.add_field(name="Location", value=job["location"], inline=True)
 if job.get("salary"):
 embed.add_field(name="Salary", value=job["salary"], inline=True)
 if job.get("requirements"):
 embed.add_field(name="Requirements", value=job["requirements"][:200] + "...", inline=False)
 embed.set_footer(text=f"Platform: {job['platform']} | Posted: {job['posted_at']}")
 return embed
 except Exception as e:
 logger.error(f"Error formatting Discord embed: {e}")
 return None

def format_telegram_message(job):
 try:
 message = f"**{job['title']}**\n"
 message += f"Company: {job['company']}\n"
 message += f"Location: {job['location']}\n"
 if job.get("salary"):
 message += f"Salary: {job['salary']}\n"
 if job.get("requirements"):
 message += f"Requirements: {job['requirements'][:200]}...\n"
 message += f"URL: {job['url']}\n"
 message += f"Platform: {job['platform']}\n"
 return message
 except Exception as e:
 logger.error(f"Error formatting Telegram message: {e}")
 return None
