from azure.data.tables import TableServiceClient, TableClient, UpdateMode
from datetime import date, datetime

# Table structure
"""
{
    PartitionKey (rfid)
    RowKey (dd-mm-yyyy)
    LastTimeFed
    portion_size
    max_feedings_per_day
    feedings_today
}
"""

# Getters and setters
def get_last_time_fed(rfid, feeding_date):
    try:
        pet = table_client.get_entity(partition_key=rfid, row_key=feeding_date)
        return pet["LastTimeFed"]
    except Exception as e:
        print(f"Error retrieving last time fed for PartitionKey '{rfid}' and RowKey '{feeding_date}': {e}")
        return None


def get_portion_size(rfid, feeding_date):
    try:
        pet = table_client.get_entity(partition_key=rfid, row_key=feeding_date)
        return pet["PortionSize"]
    except Exception as e:
        print(f"Error retrieving PortionSize for PartitionKey '{rfid}' and RowKey '{feeding_date}': {e}")
        return None


def get_connection_str(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


def check_pet_exists(rfid):
    # Query entities with the specified PartitionKey
    pet = table_client.query_entities(f"PartitionKey eq '{rfid}'")

    # Return True if any entities are found, else False
    return any(pet)


def add_pet(rfid, portion_size, max_feedings_per_day):
    entity = {
        "PartitionKey": str(rfid),  # Ensure rfid is a string
        "RowKey": todaydate,  # Use today's date
        "LastTimeFed" : datetime.now().time().isoformat(),
        "PortionSize": portion_size,
        "MaxFeedings": max_feedings_per_day,
        "FeedingsToday": 0,
    }

    # Add entity
    table_client.create_entity(entity)
    print(f"Added entity: {entity}")


# def update_pet(rfid, the_date, portion_size, max_feedings_per_day, feedings_today):
#     entity = {
#         "PartitionKey": str(rfid),  # Ensure rfid is a string
#         "RowKey": the_date,
#         "PortionSize": portion_size,
#         "MaxFeedings": max_feedings_per_day,
#         "FeedingsToday": feedings_today,  # Ensure feed count is a string
#     }
#     table_client.update_entity(entity=entity, mode=UpdateMode.REPLACE)


def update_pet_portion_size (rfid, new_portion_size = None):
    pets = table_client.query_entities(f"PartitionKey eq '{rfid}'")
    for pet in pets:
        pet["PortionSize"] = new_portion_size
        table_client.update_entity(entity=pet, mode=UpdateMode.MERGE)

def update_pet_max_feedings(rfid, new_max_feedings):
    pets = table_client.query_entities(f"PartitionKey eq '{rfid}'")
    for pet in pets:
        pet["MaxFeedings"] = new_max_feedings
        table_client.update_entity(entity=pet, mode=UpdateMode.MERGE)

# changes the number of feedings today
def update_pet_feedings_today (rfid, feeding_date):
    pet = table_client.get_entity(partition_key=rfid, row_key=feeding_date)
    if pet["FeedingsToday"] < pet["MaxFeedings"]:
        pet["FeedingsToday"] += 1
        pet["LastTimeFed"] = datetime.now().time().isoformat()
        table_client.update_entity(entity = pet, mode=UpdateMode.MERGE)
    else:
        print("TOO MUCH FEEDING")


def list_all_pets():
    pets = table_client.list_entities()
    for pet in pets:
        print(f"Listing '{pet}'")

def delete_pet_by_rfid(rfid):
    pets = table_client.query_entities(f"PartitionKey eq '{rfid}'")
    for pet in pets:
        table_client.delete_entity(partition_key=pet["PartitionKey"], row_key = pet["RowKey"])

def delete_entry (rfid, feeding_date):
    try:
        table_client.delete_entity(partition_key = rfid, row_key = feeding_date)
        print(f"Deleted entity with PartitionKey '{rfid}' and RowKey '{feeding_date}'")
    except Exception as e:
        print(f"Failed to delete pet with PartitionKey '{rfid}' and RowKey '{feeding_date}' exception '{e}'")


def delete_all_pets():
    pets = table_client.list_entities()
    for pet in pets:
        delete_entry(pet["PartitionKey"], pet["RowKey"])


# initialize connection to azure cloud
connection_string = get_connection_str("connection.txt")
table_name = "asd"


# Initialize the client
table_service_client = TableServiceClient.from_connection_string(connection_string)
table_client = table_service_client.get_table_client(table_name)

todaydate = date.today().isoformat()