import json
import requests
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient, PartitionKey
from uuid import uuid4
from config import (
    API_URL,
    AZURE_BLOB_CONTAINER_NAME,
    AZURE_STORAGE_CONNECTION_STRING,
    COSMOS_ENDPOINT,
    COSMOS_KEY,
    COSMOS_DATABASE_NAME,
    COSMOS_CONTAINER_NAME,
    RAPIDAPI_HOST,
    RAPIDAPI_KEY,
    DATE,
    LEAGUE_NAME,
    LIMIT,
)


class FetchHiglights:
  def __init__(self):
    self.query_params = {
        "date": DATE,
        "leagueName": LEAGUE_NAME,
        "limit": LIMIT
    }
    self.headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    # Initialize Azure Blob Storage
    self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    self.container_name = AZURE_BLOB_CONTAINER_NAME.lower()
    self.container_client = self.blob_service_client.get_container_client(self.container_name)

    # Initialize CosmosDB
    self.cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    self.cosmos_database = self.cosmos_client.create_database_if_not_exists(id=COSMOS_DATABASE_NAME)
    self.cosmos_container = self.cosmos_database.create_container_if_not_exists(id=COSMOS_CONTAINER_NAME, partition_key=PartitionKey(path="/id"))

  def fetch_highlights(self):
    """Fetch highlights from the API."""
    try:
        response = requests.get(API_URL, headers=self.headers, params=self.query_params, timeout=120)
        response.raise_for_status()
        highlights = response.json()
        print("Highlights fetched successfully!")
        return highlights
    except requests.exceptions.RequestException as e:
        print(f"Error fetching highlights: {e}")
        return None
  
  def save_to_blob(self, data, file_name):
    """Save highlights to Azure Blob Storage"""
    try:
        if not self.container_client.exists():
            print(f"Container {self.container_name} does not exist. Creating...")
            self.container_client.create_container()
            print(f"Container {self.container_name} created successfully.")
        else:
            print(f"Container {self.container_name} exists.")

        blob_name = f"highlights/{file_name}.json"
        blob_client = self.container_client.get_blob_client(blob_name)
        blob_client.upload_blob(json.dumps(data), overwrite=True)
        print(f"Highlights saved to Azure Blob Storage: {self.container_name}/{blob_name}")
    except Exception as e:
        print(f"Error saving to Blob Storage: {e}")

  def store_highlights_to_cosmosdb(self, highlights):
    """
    Store each highlight record into a CosmosDB table.
    Assumes that 'highlights' is a dict with a "data" key that is a list of records.
    """
    try:
        # Iterate over each highlight record and store it.
        for record in highlights.get("data", []):
            # Use the 'id' field if available, or fallback to 'url'
            item_key = record.get("id") or record.get("url")
            if item_key is None:
                # skip records without a unique identifier
                continue
            # convert the item key to a string if it's not already one
            item_key = f"{str(item_key)}_{uuid4()}"
            record['id'] = item_key # ensure the record's id field is a string

            # Optionally add the fetch date
            record["fetch_date"] = DATE
            self.cosmos_container.create_item(record)
            print(f"Stored record with key {item_key} into CosmosDB.")
    except Exception as e:
        print(f"Error storing to CosmosDB: {e}")
  
  def process_highlights(self):
    """Main function to fetch, save, and store highlights."""
    print("Fetching highlights...")
    highlights = self.fetch_highlights()
    if highlights:
        print("Saving highlights to Azure Blob Storage...")
        self.save_to_blob(highlights, "basketball_highlights")
        print("Storing highlights in CosmosDB...")
        self.store_highlights_to_cosmosdb(highlights)

if __name__ == "__main__":
    fetcher = FetchHiglights()
    fetcher.process_highlights()