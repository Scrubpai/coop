import os
from azure.storage.blob import BlobServiceClient

# Azure storage account connection string
connection_string = "DefaultEndpointsProtocol=https;AccountName=earningtranscripts;AccountKey=ogXTWgwPT1Yv4iXTIh5TY26ozaNTlrF/3REjFq2atEOl9h3ECMHaIgETAWSDOR0x4WvCohZmnqmq+AStrkQ0GQ==;EndpointSuffix=core.windows.net"

# Name of the container to retrieve files from
container_name = "aapl-ticker"

# Local directory path to save the downloaded files
local_directory = "/Users/amirk.khandani/Documents/retriever"

# Create a BlobServiceClient using the connection string
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Get a reference to the container
container_client = blob_service_client.get_container_client(container_name)

# List blobs/files in the container
blobs = container_client.list_blobs()

# Iterate over each blob/file in the container
for blob in blobs:
    # Get the blob name and construct the local file path
    blob_name = blob.name
    local_file_path = os.path.join(local_directory, blob_name)

    # Ensure the local directory structure exists
    os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

    # Download the blob/file
    with open(local_file_path, "wb") as file:
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob()
        file.write(blob_data.readall())

    print(f"Downloaded: {blob_name}")