"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/1/2024
"""
import RPi.GPIO as GPIO
import pets
from mfrc522 import SimpleMFRC522

"""
This section reads the RFID sensor and dispenses food if it is allowed
"""
#

reader = SimpleMFRC522()
try:
    print("Waiting for RFID")
    uid, text = reader.read()
    print(f"uid: '{uid}' Text: '{text}'")
    # check to see if exists in pets
    # if it exists in pets, do some more stuff
    # if it does not exist, print error stuff
finally:
    GPIO.cleanup()

