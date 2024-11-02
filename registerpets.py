import RPi.GPIO as GPIO
import pets
from mfrc522 import SimpleMFRC522


def menu():
   print(f"Choose an option.\n"
         f"1. Add pet\n"
         f"2. Remove pet\n"
         f"3. Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice (number): ")

        # Add pet
        if choice == '1':
            reader = SimpleMFRC522()
            try:
                print("Please place the RFID tag near the sensor.")
                rfid, text = reader.read()

                # check to see if exists in pets
                if not pets.check_pet_exists(rfid):
                   while True:
                       max_feedings = input("Enter the number of feedings per day: ")
                       if max_feedings.isdigit():
                           max_feedings = int(max_feedings)
                           break
                       else:
                           print("Invalid input. Please enter an integer.")
                   while True:
                       portion_size = input("Enter the portion size: ")
                       if portion_size.isdigit():
                           portion_size = int(portion_size)
                           break
                       else:
                           print("Invalid input. Please enter an integer.")
                    pets.add_pet(rfid,portion_size,max_feedings)
                else: # if pet is already in the table, return to the menu
                    print("That RFID is already registered. Please choose another option.")

            finally:
                GPIO.cleanup()

        # Remove Pet
        elif choice == '2':
            reader = SimpleMFRC522()
            try:
                print("Please place the RFID tag near the sensor.")
                rfid, text = reader.read()

                # check to see if exists in pets
                # If the pet exists, remove all entries of it.
                if pets.check_pet_exists(rfid):
                    pets.delete_pet_by_rfid(rfid)
                else:  # if pet is already in the table, return to the menu
                    print("That RFID tag is not registered. Please choose another option.")
            finally:
                GPIO.cleanup()
        elif choice == '3':
            break
        else:
            print(f"\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    print("This program removes or adds a pet to the app. You need to use the RFID tags on the RFID sensor.")
    main()