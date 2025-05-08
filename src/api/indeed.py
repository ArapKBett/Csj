import requests
from src.utils.logger import setup_logger
from src.utils.config import INDEED_API_KEY

logger = setup_logger()

def scrape_indeed_jobs():
 jobs = []
 url = "http://api.indeed.com/ads/apisearch"
 params = {
 "publisher": INDEED_API_KEY,
 "q": "cybersecurity",
 "l": "", # Global search
 "sort": "date",
 "format": "json",
 "v": "2",
 "limit": 5,
 "highlight": 0
 }
 try:
 logger.info("Starting Indeed API request")
 response = requests.get(url, params=params, timeout=10)
 response.raise_for_status()
 data = response.json()
 
 for job in data.get("results", []):
 job_data = {
 "id": job["jobkey"],
 "title": job["jobtitle"],
 "company": job["company"],
 "location": job["formattedLocation"],
 "salary": job.get("salary", "N/A"),
 "requirements": job.get("snippet", "N/A"),
 "url": job["url"],
 "platform": "Indeed",
 "posted_at": job["date"]
 }
 jobs.append(job_data)
 logger.info(f"Retrieved Indeed job: {job_data['title']}")
 
 logger.info(f"Scraped {len(jobs)} jobs from Indeed")
 except requests.exceptions.RequestException as e:
 logger.error(f"Failed to fetch Indeed jobs: {e}")
 except Exception as e:
 logger.error(f"Error processing Indeed API response: {e}")
 
 return jobs
