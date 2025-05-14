from google.cloud import storage
import os

# Initialize client
client = storage.Client()

# Reference the bucket
bucket_name = "gcp-rag"
bucket = client.bucket(bucket_name)

blobs = bucket.list_blobs(prefix="faiss_index/")

for blob in blobs:
    # Set local filename
    local_path = os.path.join("faiss_index", os.path.basename(blob.name))
    os.makedirs("faiss_index", exist_ok=True)

    # Download the file
    blob.download_to_filename(local_path)
    print(f"Downloaded: {blob.name} to {local_path}")