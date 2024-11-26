"""
This file contains functions to upload image and video files to azure storage.
"""
from azure.storage.blob import BlobServiceClient, ContentSettings


def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

connection_string = get_connection_str("connection.txt")
container_name = "pentadcontainer"


# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def upload_jpg_blob(file_path, file_in_blob_name):
    blob_client = container_client.get_blob_client(file_in_blob_name)
    # Set the content type to image/jpeg content_settings = BlobContentSettings(content_type="image/jpeg"
    content_settings = ContentSettings(content_type="image/jpeg")

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True, content_settings=content_settings)

    print(f"{file_in_blob_name} uploaded successfully.")

# Example usage
# upload_blob("/home/group3/test.txt", "test.txt")
