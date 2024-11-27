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
        print(f"Portions per feeding from database: {num_portions}")
        print(f"Previous leftover portions: {previous_leftover_portions}")
        portions_to_dispense = round(num_portions - previous_leftover_portions)
        print(f"Calculated portions to dispense: {portions_to_dispense}")
        if portions_to_dispense > 0:
            try:
                rest_api_utils.dispense_portions(portions_to_dispense)
                print("Dispense function executed successfully.")
            except Exception as e:
                print(f"Error in dispensing portions: {e}")
        else:
            print("No portions to dispense.")
        db_utils.increment_feeding_history(cursor, rfid)
        print("Feeding history updated.")
        # 拍照并上传的代码，可以根据需要启用
        # filename = db_utils.create_file_name(cursor, rfid)
        # location = 'home/group3/'
        # camera.capture_image(location, filename)
        # fileupload.upload_jpg_blob(f"{location}{filename}", filename)
    else:
        print("Pet is not eligible. Not feeding")

def handle_rfid_not_occupied(cursor, rfid, previous_leftovers_portions, leftover_portions):
    num_portions = db_utils.get_portion_per_feeding(cursor, rfid)
    portions_eaten = num_portions - leftover_portions
    print(f"Portions eaten: {portions_eaten}")
    db_utils.increment_portions_eaten_history(cursor, rfid, portions_eaten)
    print("Portions eaten history updated.")

if __name__ == "__main__":
    try:
        hx = weight_util.init_weight_sensor()
        with db_utils.mysql_connection() as connection:
            cursor = connection.cursor()
            print("This program dispenses food if an RFID tag is detected and the tag is in our database")
            occupied = False
            previous_leftovers_portions = 0
            while True:
                print("Waiting for RFID...")
                rfid, rfid_text = rfid_utils.read_rfid()
                print(f"RFID read: rfid={rfid}, rfid_text={rfid_text}")  # 添加调试信息

                if not occupied:
                    print("Feeder is not occupied. Handling pet arrival.")
                    previous_leftovers_grams = weight_util.get_weight(hx)
                    # previous_leftovers_portions = weight_util.grams_to_portions(previous_leftovers_grams) // 1
                    previous_leftovers_portions = weight_util.grams_to_portions(round(previous_leftovers_grams))
                    handle_rfid_occupied(cursor, rfid, previous_leftovers_portions)
                    connection.commit()
                    occupied = True
                else:
                    print("Feeder is occupied. Handling pet departure.")
                    leftover_grams = weight_util.get_weight(hx)
                    # leftover_portions = weight_util.grams_to_portions(leftover_grams) // 1
                    leftover_portions = weight_util.grams_to_portions(round(leftover_grams))
                    handle_rfid_not_occupied(cursor, rfid, previous_leftovers_portions, leftover_portions)
                    connection.commit()
                    occupied = False

                time.sleep(1)
    except KeyboardInterrupt:
        weight_util.cleanup()
        print("Program interrupted by user. Exiting.")
    except Exception as e:
        weight_util.cleanup()
        print("An unexpected error occurred:")
        raise
