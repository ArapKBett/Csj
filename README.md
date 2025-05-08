## Install Dependencies:

`pip3 install -r requirements.txt`

## Run the Bot:

`PYTHONPATH=$PWD python3 src/main.py`

## Access Dashboard:

Find IP:

`ifconfig`

Open `http://<termux-ip>:5000` in a browser.

## Monitor Logs:

`cat logs/bot.log`

## Test Commands:

Discord: /refresh, /filter location London, /list_jobs

Telegram: /refresh, /filter location London, /list_jobs

## Open the database:

`sqlite3 data/jobs.db`

## Run queries:

List all jobs:

`SELECT * FROM jobs ORDER BY posted_at DESC LIMIT 10;`

List Indeed jobs:

`SELECT * FROM jobs WHERE platform = 'Indeed';`

List jobs by location:

`SELECT * FROM jobs WHERE location LIKE '%London%';`

Check duplicates:

`SELECT id, title, platform, COUNT(*) as count FROM jobs GROUP BY id HAVING count > 1;`

Clear the database to remove existing duplicates:

`sqlite3 data/jobs.db "DELETE FROM jobs;"`

Exit:

`.exit`
