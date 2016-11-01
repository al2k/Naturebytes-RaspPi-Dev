#!/usr/bin/python
import time
import picamera 
from random import randint

# Let's pick a random number and use that in our testing session. We can append this number to the photograph that's saved so we know which session belongs to which
rand = randint(2,100000)

# We're using picamera to talk to the camera module and take a photo
cam = picamera.PiCamera()

# Show a live preview from the camera on the desktop and take a photo
cam.start_preview()
cam.capture("/home/pi/Desktop/Test_my_camera/naturebytes_"+ str(rand) + ".jpg")

# Wait 5 seconds and then stop the preview            
time.sleep(5)  
cam.stop_preview()

# Check the same folder (Test_my_camera) to view the photos that have been taken

# END
