"""
Pet Feeder Main File
Collaborators: Tsz Hei Chan, Ronghao Liu, Tyler Chow, Hung-Ju Ke, Nabil Mekhalfa
Last Modified: 11/1/2024
"""
import registerpets

def main_menu():
    print(f"Welcome to the pet feeder program. Please choose an option:"
          f"1. Register, unregister, or update pet"
          f"2. Upload an image or video to the cloud"
          f"3. Quit")

def main():
    while True:
        main_menu()
        choice = input("Please input an option: ")
        if choice == 1:
            registerpets.main()
        elif choice == 2:#take picture, then use fileupload.upload_blob()
            break
        elif choice == 3:
            break
        else:
            print("invalid input. Please enter a valid option.")

main()