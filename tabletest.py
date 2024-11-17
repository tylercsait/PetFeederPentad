"""
This file is used for testing purposes.
"""
from tabnanny import check
from venv import create

import db_utils
#from venv import create

#import pets_db_utils
#from datetime import date, datetime
from db_utils import *
from datetime import datetime

import registerpets

def test_registerpets_process_pet_input():
    rfid = "TEST"
    rfid_text = "ahaha"
    with mysql_connection() as cursor:
        # db_utils.create_pets_table(cursor)
        db_utils.view_table(cursor, "pets")
        registerpets.process_pet_input(cursor, rfid, rfid_text)
        db_utils.view_table(cursor, "pets")

if __name__ == "__main__":
    test_registerpets_process_pet_input()
    # with mysql_connection() as db_cursor:
        # create_pets_table(db_cursor)
        # view_table(db_cursor,"pets")
        # add_pet(db_cursor, "TEST", 0, 5, 3, 2)
        # view_table(db_cursor,"pets")
        # create_history_table(db_cursor)
        # add_history(db_cursor,"HISTORY", datetime.now().time(), 2)
        # view_table(db_cursor, "history")
        # print(check_pet_exists(db_cursor,"HISTORY"))

#todaydate = date.today().isoformat()
#pets.delete_all_pets()
# Example usage
#pets.add_pet("69", 1, 1)
#pets.add_pet("12", 2, 1)
#pets.update_pet_feedings_today("69", todaydate)
#pets.update_pet_portion_size('69', 5)
#print(pets.check_pet_exists("12"))
#delete_pet("69", todaydate)
#pets.list_all_pets()
#pets.delete_all_pets()

