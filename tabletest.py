"""
This file is used for testing purposes.
"""
from tabnanny import check
from venv import create

import db_utils
import rest_api_utils
#from venv import create
import fileupload

#import pets_db_utils
#from datetime import date, datetime
from datetime import datetime

# import registerpets

    # def test_registerpets_process_pet_input(cursor, rfid, rfid_text):
#     with mysql_connection() as cursor:
#          db_utils.create_pets_table(cursor)
#     db_utils.view_table(cursor, "pets")
#     registerpets.process_pet_input(cursor, rfid, rfid_text)


def simulate_dispense_food(cursor, rfid):#Dispense food if history is empty
    #create_history_table(cursor)
    if db_utils.eligible_to_feed(cursor, rfid):
        print("Pet is eligible. Feeding")
        db_utils.increment_feeding_history(cursor, rfid)
        rest_api_utils.dispense_portions(1)

    else:
        print("Pet not is eligible. Not feeding")


if __name__ == "__main__":
    rfid = "c"
    rfid_text = "Chris"
    with db_utils.mysql_connection() as (db_cursor, db_connection):
        # db_utils.initialize_tables(db_cursor)
        # simulate_dispense_food(db_cursor, rfid)
        # fileupload.upload_jpg_blob("C:\\users\\Tyler\\Desktop\\test.jpg",db_utils.create_file_name(db_cursor, rfid))
        # print(db_utils.create_file_name(db_cursor, "a"))
        # db_utils.add_pet(db_cursor,rfid, rfid_text, 1,1,1)
        db_utils.delete_pet_by_rfid(db_cursor,rfid)
        db_utils.view_table(db_cursor, "pets")
        db_utils.view_table(db_cursor, "history")



