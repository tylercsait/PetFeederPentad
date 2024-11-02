from azure.storage.blob import BlobServiceClient

'''
The purpose of this file is to upload image and video files to azure storage
'''

def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

connection_string = get_connection_str("connection.txt")
container_name = "pentadcontainer"

# Create the BlobServiceClient object

# Create the BlobServiceClient object
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def upload_blob(file_path, blob_name):
    blob_client = container_client.get_blob_client(blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"{blob_name} uploaded successfully.")

# Example usage
upload_blob("/home/group3/test.txt", "test.txt")
