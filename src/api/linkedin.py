import requests
from src.utils.logger import setup_logger
from src.utils.config import PROXYCURL_API_KEY

logger = setup_logger()

def scrape_linkedin_jobs():
 jobs = []
 url = "https://nubela.co/proxycurl/api/v2/linkedin/job"
 headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY }"}
 params = {
 "keyword": "cybersecurity",
 "location": "Worldwide",
 "results_limit": 5
 }
 try:
 logger.info("Starting LinkedIn Proxycurl API request")
 response = requests.get(url, headers=headers, params=params, timeout=10)
 response.raise_for_status()
 data = response.json()
 
 for job in data.get("job", []):
 job_data = {
 "id": job["job_id"],
 "title": job["job_title"],
 "company": job["company"],
 "location": job["location"],
 "salary": job.get("salary", "N/A"),
 "requirements": job.get("job_description", "N/A"),
 "url": job["job_url"],
 "platform": "LinkedIn",
 "posted_at": job["list_date"]
 }
 jobs.append(job_data)
 logger.info(f"Retrieved LinkedIn job: {job_data['title']}")
 
 logger.info(f"Scraped {len(jobs)} jobs from LinkedIn")
 except requests.exceptions.RequestException as e:
 logger.error(f"Failed to fetch LinkedIn jobs: {e}")
 except Exception as e:
 logger.error(f"Error processing LinkedIn API response: {e}")
 
 return jobs
