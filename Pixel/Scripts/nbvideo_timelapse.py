#!/usr/bin/python
# Naturebytes Wildlife Cam Kit - Video timelapse] | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes

import os
import picamera
import time
import datetime as dt

# Set the resolution of the video you intend to capture.
camera = picamera.PiCamera(resolution=(800, 600))

destination = '/media/usb0'

print "Starting up!"
time.sleep(5)
print "Waiting 60 seconds"
# Change the time.sleep value to delay the startup. The variable is in seconds, so it waits 60 seconds bef$

x = 1
y = 1
while True:
     filename = os.path.join(destination, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
     print "Taking a video. This is video %d " % (x)
     camera.start_recording(filename) 
     camera.wait_recording(5)
         # Record for 5 seconds
     camera.stop_recording()
     print "Sleeping for 5 seconds before recording again"
     time.sleep(5)
         # Waiting for 1 mins before continuing
     y += 1
     print "Done. Preparing to record next video."
     x += 1
