#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import picamera 
from random import randint

# Check that your PIR "OUT" PIN is connected to the correct PIN on the Raspberry Pi. You can confirm this in the official Naturebytes Wildlife Cam Kit instructions
sensor_pin = 13

# Let's pick a random number and use that in our testing session. We can append this number to the photograph that's saved so we know which session belongs to which
rand = randint(2,100000)

# Let's start a counter so we can mark each photo with a unique number
photo_counter = 0

# Set the GPIO (General Purpose Input Outout) PINs up and define that we want to read "sensor_pin" that we assigned above
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define the state of the PIR i.e what was it doing previously, and what is it doing now - has it triggered?
prev_state = False
curr_state = False

# We're using picamera to talk to the camera module and take a photo
cam = picamera.PiCamera()

# Start a loop and check for a change in status. Tip - wave your hand in front of the sensor to trigger it.
while True:
    time.sleep(0.1)
    prev_state = curr_state
    curr_state = GPIO.input(sensor_pin)
	
    if curr_state != prev_state:
        new_state = "HIGH so the PIR has triggered, take a photo" if curr_state else "LOW, waiting to trigger"
        print "GPIO pin %s is %s" % (sensor_pin, new_state)
        if curr_state:  # new
            cam.start_preview()
            photo_counter = photo_counter + 1
            cam.capture("/home/pi/Desktop/Test_my_camera/naturebytes_"+ str(rand) + str(photo_counter) + ".jpg")
        else:
            cam.stop_preview()
# Check the same folder (Test_my_camera) to view the photos that have been taken

# END
