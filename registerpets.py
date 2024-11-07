import RPi.GPIO as GPIO
import pets
from mfrc522 import SimpleMFRC522


def menu_registered():
   print(f"This pet is registered. Please choose an option\n"
         f"1. Update number of feedings per day.\n"
         f"2. Update portion size.\n"
         f"3. Unregister pet.\n")

def menu_not_registered():
    print(f"This pet is not registered. Would you like to register this pet?\n"
          f"1. Yes, register this pet.\n"
          f"2. input any key to exit\n")

def input_max_feedings():
    while True:
        max_feedings = input("Enter the number of feedings per day: ")
        if max_feedings.isdigit():
            max_feedings = int(max_feedings)
            break
        else:
            print("Invalid input. Please enter an integer.")
    return max_feedings


def input_portion_size():
    while True:
        portion_size = input("Portion size: ")
        if portion_size.isdigit():
            portion_size = int(portion_size)
            break
        else:
            print("Invalid input. Please enter an integer.")
    return portion_size


def main():
    reader = SimpleMFRC522()
    try:
        print("Please place the RFID tag near the sensor.")
        rfid, text = reader.read()

        # Pet is already registered. Ask to update feedings, portion size, or delete
        if pets.check_pet_exists(rfid):
            while True:
                menu_registered()
                choice = input("Please choose an option: ")

                if choice == '1':
                    max_feedings = input_max_feedings()
                    print(f"The number of feedings per day has been updated to '{max_feedings}'")
                    pets.update_pet_feedings_today(rfid, max_feedings)
                    break

                elif choice == '2':
                    portion_size = input_portion_size()
                    print(f"The portion size has been updated to '{portion_size}'")
                    pets.update_pet_portion_size(rfid, portion_size)
                    break

                elif choice == '3':
                    print(f"Unregistering pet UID '{rfid}'.")
                    pets.delete_pet_by_rfid(rfid)
                    break

                else:
                    print(f"Invalid input. Please enter a valid option.")

        # RFID is not registered. Add pet to the table
        elif not pets.check_pet_exists(rfid):
            menu_not_registered()
            choice = input("Please choose an option: ")

            if choice == '1':
                print("We will register your pet. We will need some information.")
                max_feedings = input_max_feedings()
                portion_size = input_portion_size()
                pets.add_pet(rfid,portion_size, max_feedings)
                print("Thank you, we have registered your pet.")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    print("This program removes or adds a pet to the app. You need to use the RFID tags on the RFID sensor.")
    main()