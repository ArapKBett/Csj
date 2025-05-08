from apify_client import ApifyClient
from src.utils.logger import setup_logger
from src.utils.config import APIFY_API_TOKEN

logger = setup_logger()

def scrape_glassdoor_jobs():
 jobs = []
 client = ApifyClient(APIFY_API_TOKEN)
 run_input = {
 "search": "cybersecurity",
 "location": "",
 "maxItems": 5
 }
 try:
 logger.info("Starting Glassdoor Apify API request")
 run = client.actor("apify/glassdoor-jobs-scraper").call(run_input=run_input)
 for item in client.dataset(run["defaultDatasetId"]).iterate_items():
 job_data = {
 "id": item["jobId"],
 "title": item["title"],
 "company": item["companyName"],
 "location": item["location"],
 "salary": item.get("salary", "N/A"),
 "requirements": item.get("description", "N/A"),
 "url": item["jobUrl"],
 "platform": "Glassdoor",
 "posted_at": item.get("postedDate", "N/A")
 }
 jobs.append(job_data)
 logger.info(f"Retrieved Glassdoor job: {job_data['title']}")
 
 logger.info(f"Scraped {len(jobs)} jobs from Glassdoor")
 except Exception as e:
 logger.error(f"Failed to fetch Glassdoor jobs: {e}")
 
 return jobs
