import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
from mfrc522 import SimpleMFRC522

def read_rfid():
    reader = SimpleMFRC522()
    try:
        print("Please place the RFID tag near the sensor.")
        while True:
            rfid, rfid_text = reader.read()
            return rfid, rfid_text
    finally:
        pass  # No GPIO.cleanup() here

if __name__ == "__main__":
    rfid, rfid_text = read_rfid()
    print(f"RFID: {rfid}")
    print(f"Text: {rfid_text}")
