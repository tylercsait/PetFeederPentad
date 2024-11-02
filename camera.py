import libcamera

def take_jpg():
    with libcamera.PyLibCamera() as camera:
        camera.configure()
        camera.start()

        # Capture a JPEG image
        frame = camera.capture(format='jpeg')

        # Save the image to a file
        with open('test.jpeg', 'wb') as file:
            file.write(frame)
        print("Image captured and saved as '/home/group3/test.jpeg'")

        camera.stop()
