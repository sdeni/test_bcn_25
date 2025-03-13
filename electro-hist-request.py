import os
import json
import time
import requests
import datetime
import logging

# Configure logging to output to get_data.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("electro_get_data.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Extract the authorization token into a variable
AUTH_TOKEN = "eb783848ad8ea54cd9bdd968b3b0ba8b74bbcdfc22893335293c868bc8d2b56a"

# Define common headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-GB,en;q=0.9,ru;q=0.8,uk;q=0.7,en-US;q=0.6,sq;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Priority": "u=1, i",
    "Sec-CH-UA": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Linux\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest"
}

date_to = datetime.date(2025, 3, 10)
date_from = datetime.date(2020, 3, 10)
zona = "1"
gen = "2"


url = "https://www.gpee.com.ua/main/loadCharts"

res_dir = "electro-hist"
if not os.path.exists(res_dir):
    os.makedirs(res_dir)

logger.info("Downloading history from %s to %s", date_from, date_to)

start_time = None
cur_date = date_to
actual_start_date = None
retry_count = 0
while cur_date >= date_from:
    try:
        data = {
            "date": cur_date.strftime("%d.%m.%Y"),
            "zona": zona,
            "gen": gen
        }

        file_path = os.path.join(res_dir, f"{data['date'].replace('.', '-')}_{zona}_{gen}.json")

        if os.path.exists(file_path) and os.path.getsize(file_path) > 50:
            logger.info(f"Skipping {data['date']} as it already exists.")
            cur_date -= datetime.timedelta(days=1)
            continue

        if start_time is None:
            start_time = time.time()
            actual_start_date = cur_date

        progress = float((date_to - cur_date).days / (date_to - date_from).days * 100)

        if actual_start_date != cur_date:
            estimated_time_left = (time.time() - start_time) / (actual_start_date - cur_date).days * (cur_date-date_from).days / 60
        else:
            estimated_time_left = 1000

        logger.info("Getting data for %s (%.1f%%). Estimated time left: %.1f", data['date'], progress, estimated_time_left)

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            try:
                json_data = response.json()

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                logger.info(f"Saved data to {file_path}")
            except ValueError:
                logger.error("Failed to decode JSON for %s", data['date'])
        else:
            logger.error("Failed to fetch for %s. Status code: %s", data['date'], response.status_code)

        cur_date -= datetime.timedelta(days=1)
    except Exception as e:
        logger.error("Error occurred: %s", e)

        if retry_count > 3:
            logger.error("Too many retries. Go for the next date.")
            cur_date -= datetime.timedelta(days=1)
            retry_count = 0
        else:
            retry_count += 1
            logger.info("Retrying...")
            time.sleep(5)
