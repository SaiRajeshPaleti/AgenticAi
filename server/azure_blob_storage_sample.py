import os
# Minimal script to read sample data from Azure Blob Storage using Azure SDK
from azure.storage.blob import BlobServiceClient

def main():
    const_strring = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not const_strring:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set.")
        returns
    try:
        blob_service_client = BlobServiceClient.from_connection_string(const_strring)
        container_client = blob_service_client.get_container_client('agenticai-demo-data')
        blob_client = container_client.get_blob_client('agentic ai demo prep work.txt')
# Replace with your actual connection string, container, and blob names
        data = blob_client.download_blob().readall()
        print(data.decode('utf-8'))
    except Exception as e:
        print(f"Error accessing Azure Blob Storage: {e}")
if __name__ == "__main__":
    main()  


