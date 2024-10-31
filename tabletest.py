from azure.data.tables import TableServiceClient, TableClient
from datetime import date

# Table structure
"""
{
    PartitionKey (rfid)
    RowKey (dd-mm-yyyy)
    portion_size
    max_feedings_per_day
    feedings_today
}
"""

def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


def add_pet(rfid, portion_size, max_feedings_per_day):
    entity = {
        "PartitionKey": str(rfid),  # Ensure rfid is a string
        "RowKey": todaydate,  # Use today's date
        "PortionSize": portion_size,
        "MaxFeedings": max_feedings_per_day,
        "FeedingsToday": "0",  # Ensure feed count is a string
    }

    # Add entity
    table_client.create_entity(entity)
    print(f"Added entity: {entity}")

def delete_pet (rfid, date_key):
    table_client.delete_entity(partition_key = rfid,row_key = date_key)
    print(f"Deleted entity with PartitionKey '{rfid}' and RowKey '{date_key}'")

connection_string = get_connection_str("connection.txt")
table_name = "asd"
todaydate = date.today().isoformat()

# Initialize the client
table_service_client = TableServiceClient.from_connection_string(connection_string)
table_client = table_service_client.get_table_client(table_name)

# Example usage
add_pet("69", 1, 1)
delete_pet("69", todaydate)
