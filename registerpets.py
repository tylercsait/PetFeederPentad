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

        if choice == '1':
            reader = SimpleMFRC522()
            try:
                print("Please place the RFID tag near the sensor.")
                rfid, text = reader.read()
                # check to see if exists in pets
                # if it exists in pets, do some more stuff
                # if it does not exist, print error stuff
            finally:
                GPIO.cleanup()
        elif choice == '2':
            break
        elif choice == '3':
            break
        else:
            print(f"\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()