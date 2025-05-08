import requests
from bs4 import BeautifulSoup
import uuid
import time
from src.utils.logger import setup_logger

logger = setup_logger()

def scrape_cryptojobslist_jobs():
 jobs = []
 url = "https://cryptojobslist.com/jobs?query=cybersecurity"
 headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
 }
 try:
 logger.info("Starting CryptoJobsList scraping")
 response = requests.get(url, headers=headers, timeout=10)
 response.raise_for_status()
 soup = BeautifulSoup(response.text, "html.parser")
 
 job_cards = soup.select(".job-listing")
 for card in job_cards[:5]:
 title_elem = card.select_one(".job-title")
 company_elem = card.select_one(".company-name")
 location_elem = card.select_one(".job-location")
 link_elem = card.select_one("a.job-link")
 
 if title_elem and company_elem and link_elem:
 job_data = {
 "id": str(uuid.uuid4()), # No job ID in HTML, use UUID
 "title": title_elem.text.strip(),
 "company": company_elem.text.strip(),
 "location": location_elem.text.strip() if location_elem else "N/A",
 "salary": "N/A",
 "requirements": "N/A",
 "url": link_elem["href"],
 "platform": "CryptoJobsList",
 "posted_at ": "N/A"
 }
 jobs.append(job_data)
 logger.info(f"Scraped CryptoJobsList job: {job_data['title']}")
 time.sleep(1)
 
 logger.info(f"Scraped {len(jobs)} jobs from CryptoJobsList")
 except requests.exceptions.RequestException as e:
 logger.error(f"Failed to scrape CryptoJobsList: {e}")
 except Exception as e:
 logger.error(f"Error processing CryptoJobsList: {e}")
 
 return jobs
