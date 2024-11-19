"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/17/2024
"""

import weight_util
import mysql.connector
import db_utils
import rfid_utils
import rest_api_utils
import time

GRAMS_PER_PORTION = 8 # 7-9 grams per portion, 8 is the middle

if __name__ == "__main__":
    with db_utils.mysql_connection() as db_cursor:
        print("This program dispenses food if an RFID tag is detected and the tag is in our database")
        try:
            while True:
                rfid, rfid_text = rfid_utils.read_rfid()
                # Check if eligible to feed
                if db_utils.eligible_to_feed(db_cursor, rfid):
                    print("Pet is eligible. Feeding")
                    num_portions = db_utils.get_portion_per_feeding(db_cursor, rfid)
                    rest_api_utils.dispense_portions(num_portions)
                    db_utils.increment_feeding_history(db_cursor, rfid)

                else:
                    print("Pet is not eligible. Not feeding")

                # Optional: Add a small delay to avoid rapid looping
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program interrupted by user. Exiting.")
