from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

def upload_data():
    client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    
    # Create container
    try:
        client.create_container(CONTAINER_NAME)
        print("Container created!")
    except:
        print("Container already exists")
    
    # Upload file
    blob_client = client.get_blob_client(
        container=CONTAINER_NAME, 
        blob="raw/sales_data.csv"
    )
    
    with open("data/sales_data.csv", "rb") as f:
        blob_client.upload_blob(f, overwrite=True)
    
    print("Data uploaded successfully!")

if __name__ == "__main__":
    upload_data()