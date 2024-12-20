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
            # Once an RFID is read, return the values
            return rfid, rfid_text
    finally:
        # 不要在这里调用 GPIO.cleanup()
        # 如果需要，可以释放与 RFID 相关的资源
        pass  # 或者调用 reader.GPIO_CLEENUP()，如果该方法仅清除 RFID 相关的 GPIO
