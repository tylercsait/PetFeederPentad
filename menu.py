"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/1/2024
"""
import registerpets
import camera
import fileupload

def main_menu():
    print(f"\nWelcome to the pet feeder program. Please choose an option:\n"
          f"1. Register, unregister, or update pet\n"
          f"2. Upload an image or video to the cloud\n"
          f"3. Quit\n")

def main():
    while True:
        main_menu()
        choice = input(f"Please input an option: ")
        if choice == '1':
            registerpets.main()
        elif choice == '2':#take picture, then use fileupload.upload_blob()
            camera.capture_image()
            fileupload.upload_jpg_blob('/home/group3/test.jpg', 'test.jpg')
        elif choice == '3':
            break
        else:
            print(f"{choice} is an invalid input. Please enter a valid option.")

main()