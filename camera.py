from picamera2 import Picamera2

def capture_image(location, filename):
    try:
        picam2 = Picamera2()
        config = picam2.create_still_configuration()
        picam2.configure(config)
        picam2.start()
        picam2.capture_file(f'{location}{filename}')
        picam2.stop()
        print(f"Image captured and saved as '{location}{filename}'")
    finally:
        picam2.close()


if __name__ == "__main__":
    capture_image()

