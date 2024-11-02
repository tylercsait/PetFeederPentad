from picamera2 import Picamera2

def capture_image():
    picam2 = Picamera2()
    config = picam2.create_still_configuration()
    picam2.configure(config)
    picam2.start()
    picam2.capture_file('/home/group3/test.jpg')
    picam2.stop()
    print("Image captured and saved as '/home/group3/test.jpg'")

if __name__ == "__main__":
    capture_image()

