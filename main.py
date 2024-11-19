"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/17/2024
"""

import weight_util
import mysql.connector
import db_utils
import rfid_utils
import time

if __name__ == "__main__":
    with db_utils.mysql_connection() as db_cursor:
        print("This program removes or adds a pet to the app. You need to use the RFID tags on the RFID sensor.")
        try:
            while True:
                rfid, rfid_text = rfid_utils.read_rfid()
                # Check if eligible to feed
                if db_utils.eligible_to_feed(db_cursor, rfid):
                    print("Pet is eligible. Feeding")
                    db_utils.increment_feeding_history(db_cursor, rfid)
                else:
                    print("Pet is not eligible. Not feeding")

                # Optional: Add a small delay to avoid rapid looping
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program interrupted by user. Exiting.")
