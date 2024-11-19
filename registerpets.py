#import RPi.GPIO as GPIO
import db_utils
#from mfrc522 import SimpleMFRC522

from sqltest import mysql_connection


def menu_registered():
   print(f"This pet is registered. Please choose an option\n"
         f"1. Update number of meals per day.\n"
         f"2. Update number of portions per meal.\n"
         f"3. Update the pet's name.\n"
         f"4. Unregister pet.\n")

def menu_not_registered():
    print(f"This pet is not registered. Would you like to register this pet?\n"
          f"1. Yes, register this pet.\n"
          f"2. input any key to exit\n")

def input_max_feedings_per_day():
    while True:
        max_feedings = input("Enter the maximum number of meals per day: ")
        if max_feedings.isdigit():
            max_feedings = int(max_feedings)
            break
        else:
            print("Invalid input. Please enter an integer.")
    return max_feedings


def input_max_portions_per_day():
    while True:
        portion_size = input("How many portions the pet will eat a day: ")
        if portion_size.isdigit():
            portion_size = int(portion_size)
            break
        else:
            print("Invalid input. Please enter an integer.")
    return portion_size

def input_portion_per_feeding():
    while True:
        portion_size = input("Portion per meal: ")
        if portion_size.isdigit():
            portion_size = int(portion_size)
            break
        else:
            print("Invalid input. Please enter an integer.")
    # Calculate the max_portions_per_day here?
    return portion_size

def input_pet_name():
    while True:
        new_name = input("What would you like to name your pet?: ")
        confirmation = input(f"Is {new_name} correct? y/n: \n")
        if confirmation == "y":
            break
    return new_name





def process_pet_input(cursor, rfid, rfid_text):
    #db_utils.create_pets_table(cursor)

    # If the Pet is already registered. Ask to update feedings, portion size, or delete
    if db_utils.check_pet_exists(cursor, rfid, "pets"):
        while True:
            menu_registered()
            choice = input("Please choose an option: ")

            if choice == '1':
                max_feedings = input_max_feedings_per_day()
                print(f"The maximum number of meals per day has been updated to '{max_feedings}'")
                db_utils.update_pet_feedings_today(cursor, rfid, max_feedings)
                break

            elif choice == '2':
                portion_per_feedings = input_portion_per_feeding()
                print(f"The number of portions per meal has been updated to '{portion_per_feedings}'")
                db_utils.update_pet_portion_size(cursor, rfid, portion_per_feedings)
                break

            elif choice == '3':
                new_name = input_pet_name()
                print(f"The pet's name has been updated to '{new_name}'")
                db_utils.update_pet_name(cursor, rfid, new_name)
                break

            elif choice == '4':
                print(f"Unregistering pet UID '{rfid}'.")
                db_utils.delete_pet_by_rfid(cursor, rfid)
                break

            else:
                print(f"Invalid input. Please enter a valid option.")

        # RFID is not registered. Add pet to the table
    elif not db_utils.check_pet_exists(cursor, rfid, "pets"):
        menu_not_registered()
        choice = input("Please choose an option: ")

        if choice == '1':
            print("We will register your pet. We will need some information.")
            max_feedings = input_max_feedings_per_day()
            portion_per_feedings = input_portion_per_feeding()
            max_portions_per_day = max_feedings * portion_per_feedings
            db_utils.add_pet(cursor, rfid, rfid_text, portion_per_feedings, max_feedings, max_portions_per_day)
            print("Thank you, we have registered your pet.")

def read_rfid():
    reader = SimpleMFRC522()
    try:
        rfid, rfid_text = reader.read()
        return rfid, rfid_text
    finally:
        GPIO.cleanup()

# def main(cursor):
#     reader = SimpleMFRC522()
#     try:
#         print("Please place the RFID tag near the sensor.")
#         rfid, rfid_text = reader.read()
#         process_pet_input(cursor,rfid,rfid_text)
#
#     finally:
#         GPIO.cleanup()


if __name__ == "__main__":
    with mysql_connection() as db_cursor:
        print("This program removes or adds a pet to the app. You need to use the RFID tags on the RFID sensor.")
        read_rfid(db_cursor)
