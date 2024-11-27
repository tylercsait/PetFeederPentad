"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/17/2024
"""

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
print(f"Main: Current GPIO mode: {GPIO.getmode()}")  # 调试信息

import weight_util
import mysql.connector
import db_utils
import rfid_utils
import rest_api_utils
import time
import camera
import fileupload

def handle_rfid_occupied(cursor, rfid, previous_leftover_portions):
    if db_utils.eligible_to_feed(cursor, rfid):
        print("Pet is eligible. Feeding")
        num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
        # round down leftover portions
        print("1")
        rest_api_utils.dispense_portions(num_portions - previous_leftover_portions)
        print("2")
        db_utils.increment_feeding_history(cursor, rfid)
        print("3")

        filename = db_utils.create_file_name(cursor, rfid)
        location = 'home/group3/'
        # Then take a picture and upload it
        # camera.capture_image(location, filename)
        # fileupload.upload_jpg_blob(f"{location}{filename}", filename)

    else:
        print("Pet is not eligible. Not feeding")

def handle_rfid_not_occupied(cursor, rfid, previous_leftovers, leftovers):
    num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
    portions_eaten = num_portions - leftovers
    db_utils.increment_portions_eaten_history(cursor, rfid, portions_eaten)

if __name__ == "__main__":
    try:
        hx = weight_util.init_weight_sensor()
        with db_utils.mysql_connection() as db_cursor:
            print("This program dispenses food if an RFID tag is detected and the tag is in our database")
            occupied = False
            leftover = 0
            previous_leftovers_portions = 0
            calculated_weight = 0
            while True:
                print("Waiting for RFID...")
                rfid, rfid_text = rfid_utils.read_rfid()
                print(f"RFID read: rfid={rfid}, rfid_text={rfid_text}")  # 添加调试信息

                if not occupied:
                    print("Feeder is not occupied. Handling pet arrival.")
                    previous_leftovers_grams = weight_util.get_weight(hx)
                    previous_leftovers_portions = weight_util.grams_to_portions(previous_leftovers_grams) // 1
                    handle_rfid_occupied(db_cursor, rfid, previous_leftovers_portions)
                    occupied = True
                elif occupied:
                    print("Feeder is occupied. Handling pet departure.")
                    leftover_grams = weight_util.get_weight(hx)
                    leftover_portions = weight_util.grams_to_portions(leftover_grams) // 1
                    handle_rfid_not_occupied(db_cursor, rfid, previous_leftovers_portions, leftover_portions)
                    occupied = False

                time.sleep(1)
    except KeyboardInterrupt:
        weight_util.cleanup()
        print("Program interrupted by user. Exiting.")
    except Exception as e:
        weight_util.cleanup()
        print("An unexpected error occurred:")
        raise  # 重新抛出异常，显示完整的堆栈跟踪
