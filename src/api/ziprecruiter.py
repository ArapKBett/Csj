import requests
from src.utils.logger import setup_logger
from src.utils.config import ZIPRECRUITER_API_KEY

logger = setup_logger()

def scrape_ziprecruiter_jobs():
 jobs = []
 url = "https://api.ziprecruiter.com/jobs/v1"
 params = {
 "api_key": ZIPRECRUITER_API_KEY,
 "search": "cybersecurity",
 "location": "",
 "jobs_per_page": 5,
 "page": 1
 }
 try:
 logger.info("Starting ZipRecruiter API request")
 response = requests.get(url, params=params, timeout=10)
 response.raise_for_status()
 data = response.json()
 
 for job in data.get("jobs", []):
 job_data = {
 "id": job["id"],
 "title": job["name"],
 "company": job["hiring_company"]["name"],
 "location": job["location"],
 "salary": job.get("salary", "N/A"),
 "requirements": job.get("snippet", "N/A"),
 "url": job["url"],
 "platform": "ZipRecruiter",
 "posted_at": job["posted_time"]
 }
 jobs.append(job_data)
 logger.info(f"Retrieved ZipRecruiter job: {job_data['title']}")
 
 logger.info(f"Scraped {len(jobs)} jobs from ZipRecruiter")
 except requests.exceptions.RequestException as e:
 logger.error(f"Failed to fetch ZipRecruiter jobs: {e}")
 except Exception as e:
 logger.error(f"Error processing ZipRecruiter API response: {e}")
 
 return jobs
