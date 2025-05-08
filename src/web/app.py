from flask import Flask, render_template, request, flash, redirect, url_for
from src.utils.database import JobDatabase
from src.utils.logger import setup_logger
from src.utils.config import FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
db = JobDatabase()
logger = setup_logger()

@app.route("/")
def index():
 platform = request.args.get("platform")
 location = request.args.get("location")
 jobs = db.query_jobs(platform=platform, location=location)
 return render_template("index.html", jobs=jobs)

@app.route("/clear_jobs", methods=["POST"])
def clear_jobs():
 try:
 db.conn.execute("DELETE FROM jobs")
 db.conn.commit()
 flash("All jobs cleared from database")
 logger.info("Cleared all jobs from database")
 except Exception as e:
 flash(f"Error clearing jobs: {e}")
 logger.error(f"Error clearing jobs: {e}")
 return redirect(url_for("index"))

def run_flask_app():
 try:
 logger.info("Starting Flask web dashboard")
 app.run(host="0.0.0.0", port=5000, debug=False)
 except Exception as e:
 logger.error(f"Flask app crashed: {e}", exc_info=True)
