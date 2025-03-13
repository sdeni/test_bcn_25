import os
import json
import requests
import logging

# Configure logging to output to get_data.log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("get_data.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Extract the authorization token into a variable
AUTH_TOKEN = "eb783848ad8ea54cd9bdd968b3b0ba8b74bbcdfc22893335293c868bc8d2b56a"

# Define common headers
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9,ru;q=0.8,uk;q=0.7,en-US;q=0.6,sq;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Domain": "sardegnarcheologica.it",
    "Priority": "u=1, i",
    "Sec-CH-UA": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"Linux\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Authorization": AUTH_TOKEN,
    "Referer": "https://sardegnarcheologica.it/nuraghe/0/en"
}

# Filename for the main list
list_filename = "main.json"
places = None

# Check if main.json exists; if so, load the data, otherwise download it.
if os.path.exists(list_filename):
    logger.info(f"{list_filename} already exists. Loading data from file.")
    with open(list_filename, "r", encoding="utf-8") as f:
        places = json.load(f)
else:
    logger.info("Downloading list of objects...")
    list_url = "https://sardegnarcheologica.it/api/website/en/nuraghi/list"
    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        logger.error("Failed to fetch list. Status code: %s", response.status_code)
        exit()

    raw_text = response.text
    start_index = raw_text.find('[')
    if start_index == -1:
        logger.error("Could not find JSON array in the response.")
        exit()

    json_str = raw_text[start_index:]
    try:
        places = json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON: %s", e)
        exit()

    with open(list_filename, "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    logger.info("Saved %s with %d objects.", list_filename, len(places))

# Create folder 'items' if it doesn't exist
os.makedirs("items", exist_ok=True)

# Iterate through each place and fetch its detailed data
for idx, place in enumerate(places):
    object_id = place.get("id")
    logger.info("Fetching details for id %s (%d/%d)...", object_id, idx + 1, len(places))
    if not object_id:
        logger.error("No object ID for item %d", idx + 1)
        continue

    filename = os.path.join("items", f"{object_id}.json")
    if os.path.exists(filename):
        logger.info("Skipping id %s, already fetched.", object_id)
        continue

    detail_url = f"https://sardegnarcheologica.it/api/website/en/detail/{object_id}"
    detail_response = requests.get(detail_url, headers=headers)
    if detail_response.status_code != 200:
        logger.error("Failed to fetch details for id %s. Status code: %s", object_id, detail_response.status_code)
        continue

    detail_text = detail_response.text
    # Check and remove potential prefix if present
    if detail_text.startswith(")]}',"):
        idx2 = detail_text.find('[')
        detail_text = detail_text[idx2:]

    try:
        detail_data = json.loads(detail_text)
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON for id %s: %s", object_id, e)
        continue

    # Save the detailed data to items/{id}.json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(detail_data, f, ensure_ascii=False, indent=2)
    logger.info("Saved details for id %s to %s.", object_id, filename)
