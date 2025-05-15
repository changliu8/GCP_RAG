from google.cloud import storage
import os

# Set your GCS bucket name and directory
BUCKET_NAME = "gcp-rag"
GCS_DIR = "faiss_index/"
LOCAL_DIR = "faiss_index/"


# Initialize GCS client
client = storage.Client()

# Get the bucket
bucket = client.bucket(BUCKET_NAME)

# Create local directory if it doesn't exist
os.makedirs(LOCAL_DIR, exist_ok=True)

# List and download blobs
blobs = bucket.list_blobs(prefix=GCS_DIR)
for blob in blobs:
    if blob.name.endswith("/"):
        continue  # Skip directories
    filename = blob.name[len(GCS_DIR):]  # Strip folder prefix
    local_path = os.path.join(LOCAL_DIR, filename)

    # Create subdirectories if needed
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # Download file
    blob.download_to_filename(local_path)
    print(f"Downloaded: {blob.name} -> {local_path}")