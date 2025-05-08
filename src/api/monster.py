from apify_client import ApifyClient
from src.utils.logger import setup_logger
from src.utils.config import APIFY_API_TOKEN

logger = setup_logger()

def scrape_monster_jobs():
 jobs = []
 client = ApifyClient(APIFY_API_TOKEN)
 run_input = {
 "query": "cybersecurity",
 "location": "",
 "maxItems": 5
 }
 try:
 logger.info("Starting Monster Apify API request")
 run = client.actor("apify/monster-jobs-scraper").call(run_input=run_input)
 for item in client.dataset(run["defaultDatasetId"]).iterate_items():
 job_data = {
 "id": item["jobId"],
 "title": item["title"],
 "company": item["company"],
 "location": item["location"],
 "salary": item.get("salary", "N/A"),
 "requirements": item.get("description", "N/A"),
 "url": item["url"],
 "platform": "Monster",
 "posted_at": item.get("postedDate", "N/A")
 }
 jobs.append(job_data)
 logger.info(f"Retrieved Monster job: {job_data['title']}")
 
 logger.info(f"Scraped {len(jobs)} jobs from Monster")
 except Exception as e:
 logger.error(f"Failed to fetch Monster jobs: {e}")
 
 return jobs
