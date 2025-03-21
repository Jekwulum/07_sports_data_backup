# process_videos.py
import json
import requests
from io import BytesIO
from azure.storage.blob import BlobServiceClient
from uuid import uuid4

from config import (
    AZURE_BLOB_CONTAINER_NAME,
    AZURE_STORAGE_CONNECTION_STRING,
    INPUT_KEY,
    OUTPUT_KEY_PREFIX,
)

def process_videos():
    """
    Fetch the highlights from Azure Blob Storage. 
    Iterate over all the video URLs, and download each video, and upload them back to Azure Blob Storage.
    """
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_name = AZURE_BLOB_CONTAINER_NAME.lower()

        print("Fetching the JSON file from Azure Blob Storage...")
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(INPUT_KEY)
        blob_data = blob_client.download_blob()

        json_content = blob_data.readall().decode('utf-8')
        highlights = json.loads(json_content)

        # Process each highlight record that has a video URL
        videos = highlights.get("data", [])
        print(f"Found {len(videos)} videos in the JSON file.")
        if not videos:
            print("No videos found in the JSON file.")
            return
        
        for index, record in enumerate(videos):
          video_url = record.get("url")
          if not video_url:
            print(f"Record {index} does not contain a video URL. Skipping.")
            continue
        
          print(f"Processing video {index}: {video_url}")

          # Download the video
          video_response = requests.get(video_url, stream=True)
          video_response.raise_for_status()

          # Prepare the video data (BytesIO is optional here; you can use video_response.content directly)
          video_data = BytesIO(video_response.content)
          
          # Create a unique key for each video (e.g., videos/highlight_0.mp4, videos/highlight_1.mp4, etc.)
          unique_id = uuid4()
          output_key = f"{OUTPUT_KEY_PREFIX}highlight_{index}_{unique_id}.mp4"

          # Upload the video to Azure Blob Storage
          output_blob_client = container_client.get_blob_client(output_key)
          output_blob_client.upload_blob(video_data, overwrite=True)
          print(f"Video {index} uploaded successfully to Azure Blob Storage: {container_name}/{output_key}")

    except Exception as e:
        print(f"Error processing videos: {e}")
        return None

if __name__ == "__main__":
    process_videos()