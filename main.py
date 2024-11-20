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
import camera
import fileupload
GRAMS_PER_PORTION = 8 # 7-9 grams per portion, 8 is the middle

def handle_rfid(cursor, rfid):
    if db_utils.eligible_to_feed(cursor, rfid):
        print("Pet is eligible. Feeding")
        num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
        rest_api_utils.dispense_portions(num_portions)
        db_utils.increment_feeding_history(cursor, rfid)

        # Then take a picture and upload it
        # camera.capture_image()
        # fileupload.upload_jpg_blob("/home/group3/test.jpeg", "test.jpg")

    else:
        print("Pet is not eligible. Not feeding")

if __name__ == "__main__":
    with db_utils.mysql_connection() as db_cursor:
        print("This program dispenses food if an RFID tag is detected and the tag is in our database")
        try:
            occupied = False
            while True:
                rfid, rfid_text = rfid_utils.read_rfid()
                # Check if eligible to feed
                if not occupied:
                    handle_rfid(db_cursor, rfid)
                    occupied = True
                elif occupied:
                    occupied = False

                # Optional: Add a small delay to avoid rapid looping
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program interrupted by user. Exiting.")
