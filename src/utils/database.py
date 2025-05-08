import sqlite3
from src.utils.logger import setup_logger

logger = setup_logger()

class JobDatabase:
 def __init__(self):
 self.conn = sqlite3.connect("data/jobs.db", check_same_thread=False)
 self.create_table()
 
 def create_table(self):
 try:
 self.conn.execute("""
 CREATE TABLE IF NOT EXISTS jobs (
 id TEXT PRIMARY KEY,
 title TEXT,
 company TEXT,
 location TEXT,
 salary TEXT,
 requirements TEXT,
 url TEXT,
 platform TEXT,
 posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 )
 """)
 self.conn.commit()
 logger.info("Database table created or verified")
 except Exception as e:
 logger.error(f"Error creating database table: {e}")
 
 def job_exists(self, job_id):
 try:
 cursor = self.conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,))
 exists = cursor.fetchone() is not None
 logger.info(f"Checked job ID {job_id}: {'exists' if exists else 'does not exist'}")
 return exists
 except Exception as e:
 logger.error(f"Error checking job existence: {e}")
 return False
 
 def add_job(self, job_id, title, company, location, salary, requirements, url, platform):
 try:
 self.conn.execute("""
 INSERT INTO jobs (id, title, company, location, salary, requirements, url, platform)
 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
 """, (job_id, title, company, location, salary, requirements, url, platform))
 self.conn.commit()
 logger.info(f"Added job to database: {title}")
 except Exception as e:
 logger.error(f"Error adding job to database: {e}")
 
 def get_recent_jobs(self, limit=10):
 try:
 cursor = self.conn.execute("SELECT * FROM jobs ORDER BY posted_at DESC LIMIT ?", (limit,))
 return cursor.fetchall()
 except Exception as e:
 logger.error(f"Error fetching recent jobs: {e}")
 return []
 
 def query_jobs(self, platform=None, location=None):
 try:
 query = "SELECT * FROM jobs WHERE 1=1"
 params = []
 if platform:
 query += " AND platform = ?"
 params.append(platform)
 if location:
 query += " AND location LIKE ?"
 params.append(f"%{location}%")
 query += " ORDER BY posted_at DESC"
 cursor = self.conn.execute(query, params)
 return cursor.fetchall()
 except Exception as e:
 logger.error(f"Error querying jobs: {e}")
 return []
