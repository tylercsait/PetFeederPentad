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
import weight_util
import camera
import fileupload

# REST_URL = "http://192.168.1.200:8123/api/services/number/set_value"
REST_URL = "http://192.168.66.200:8123/api/services/number/set_value"


def handle_rfid_occupied(cursor, rfid, previous_leftover_portions):
    if db_utils.eligible_to_feed(cursor, rfid):
        print("Pet is eligible. Feeding")
        num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
        print(f"Num portions: {num_portions}, Previous leftover portions: {previous_leftover_portions}")

        # Ensure previous_leftover_portions is non-negative
        previous_leftover_portions = max(previous_leftover_portions, 0)

        # Calculate the portions to dispense
        portions_to_dispense = num_portions - previous_leftover_portions
        print(f"Calculated portions to dispense: {portions_to_dispense}")

        if portions_to_dispense > 0:
            print(f"Dispensing {portions_to_dispense} portions.")
            rest_api_utils.dispense_portions(portions_to_dispense)
        else:
            print("No portions to dispense.")

        db_utils.increment_feeding_history(cursor, rfid)
        print("Feeding history updated.")

        filename = db_utils.create_file_name(cursor, rfid)
        location = '/home/group3/'
        # Then take a picture and upload it
        camera.capture_image(location, filename)
        fileupload.upload_jpg_blob(f"{location}{filename}", filename)
        print(f"Image captured and uploaded as '{filename}'")
    else:
        print("Pet is not eligible. Not feeding")

def handle_rfid_not_occupied(cursor, rfid, previous_leftovers, leftovers):
    num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
    portions_eaten = num_portions - leftovers
    print(f"Previous leftovers: {previous_leftovers}, Leftovers: {leftovers}, Portions eaten: {portions_eaten}")

    # Ensure leftovers are non-negative
    leftovers = max(leftovers, 0)

    db_utils.increment_portions_eaten_history(cursor, rfid, portions_eaten)
    print("Portions eaten history updated.")

if __name__ == "__main__":
    hx = weight_util.init_weight_sensor()
    with db_utils.mysql_connection() as (db_cursor, db_connection):
        print("This program dispenses food if an RFID tag is detected and the tag is in our database")
        try:
            occupied = False
            previous_leftovers_portions = 0
            while True:
                rfid, rfid_text = rfid_utils.read_rfid()
                print(f"RFID detected: {rfid}")

                # Check if eligible to feed
                if not occupied:
                    previous_leftovers_grams = weight_util.get_weight(hx)
                    previous_leftovers_portions = weight_util.grams_to_portions(previous_leftovers_grams) // 1
                    previous_leftovers_portions = max(previous_leftovers_portions, 0)
                    print(f"Previous leftovers (grams): {previous_leftovers_grams}, Previous leftovers (portions): {previous_leftovers_portions}")
                    handle_rfid_occupied(db_cursor, rfid, previous_leftovers_portions)
                    db_connection.commit()
                    occupied = True
                    print("Occupied set to True.")
                elif occupied:
                    leftover_grams = weight_util.get_weight(hx)
                    leftover_portions = weight_util.grams_to_portions(leftover_grams) // 1
                    leftover_portions = max(leftover_portions, 0)
                    print(f"Leftover (grams): {leftover_grams}, Leftover (portions): {leftover_portions}")
                    handle_rfid_not_occupied(db_cursor, rfid, previous_leftovers_portions, leftover_portions)
                    db_connection.commit()
                    occupied = False
                    print("Occupied set to False.")
                # Optional: Add a small delay to avoid rapid looping
                time.sleep(1)
        except KeyboardInterrupt:
            weight_util.cleanup()
            print("Program interrupted by user. Exiting.")
        except Exception as e:
            weight_util.cleanup()
            print("Program interrupted by user. Exiting.")
            raise
