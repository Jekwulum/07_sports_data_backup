import os
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

###################################
# RapidAPI & Fetch-Related Config
###################################
API_URL = os.getenv("API_URL", "https://sport-highlights-api.p.rapidapi.com/basketball/highlights")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "sport-highlights-api.p.rapidapi.com")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")  # No default, must be set at runtime

# Use the current day in YYYY-MM-DD format as the default date
DATE = os.getenv("DATE", datetime.utcnow().strftime("%Y-%m-%d"))
LEAGUE_NAME = os.getenv("LEAGUE_NAME", "NCAA")
LIMIT = int(os.getenv("LIMIT", "10"))

###################################
# COSMOSDB
###################################
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE_NAME = os.getenv("COSMOS_DATABASE_NAME", "highlights")
COSMOS_CONTAINER_NAME = os.getenv("COSMOS_CONTAINER_NAME", "basketballhighlights")

###################################
# Azure Blob Storage Settingsr
###################################
AZURE_BLOB_CONTAINER_NAME = os.getenv("AZURE_BLOB_CONTAINER_NAME")
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

###################################
# Video Paths in S3
###################################
INPUT_KEY = os.getenv("INPUT_KEY", "highlights/basketball_highlights.json")
# Note: For multiple videos, you may want to use a key pattern rather than a fixed name.
OUTPUT_KEY_PREFIX = os.getenv("OUTPUT_KEY_PREFIX", "videos/")

###################################
# run_all.py Retry/Delay Config
###################################
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "30"))
WAIT_TIME_BETWEEN_SCRIPTS = int(os.getenv("WAIT_TIME_BETWEEN_SCRIPTS", "60"))