#!/usr/bin/python
# Naturebytes Wildlife Cam Kit - Video by PIR | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes

import RPi.GPIO as GPIO
import time
from subprocess import call
from datetime import datetime
import logging

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live 

logging.basicConfig(format='%(asctime)s %(message)s',filename='naturebytes_camera_log',level=logging.DEBUG)
logging.info('Naturebytes Wildlife Cam Kit started up successfully')

# Assigning a variable to the pins that we have connected the PIR to
sensorPin = 13

# Ir add 
irPin = 16

# Setting the GPIO (General Purpose Input Output) pins up so we can detect if they are HIGH or LOW (on or off)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#config IR
GPIO.setup(irPin, GPIO.OUT, initial=0)

# GPIO.setup(lowbattPin, GPIO.IN)

# Defining our default states so we can detect a change

prevState = False
currState = False

# Starting a loop

while True:
    time.sleep(0.1)
    prevState = currState
    # prevBattState = currBattState
    
    # Map the state of the camera to our input pins (jumper cables connected to your PIR)

    currState = GPIO.input(sensorPin)
    # currBattState = GPIO.input(lowbattPin)

    # Checking that our state has changed
   
    if currState != prevState:
    # About to check if our new state is HIGH or LOW

        newState = "HIGH" if currState else "LOW"
   
        print "GPIO pin %s is %s" % (sensorPin, newState)
        # print "Battery level detected via pin %s is %s" % (lowbattPin, newBattState)

        if currState:  # Our state has changed, so that must be a trigger from the PIR       
     
            i = datetime.now() # Get the time now
            get_date = i.strftime('%Y-%m-%d') # Get and format the date
            get_time = i.strftime('%H-%M-%S.%f') # Get and format the time

            # Recording that a PIR trigger was detected
            logging.info('PIR trigger detected')
            
            # Turn on IR
            GPIO.output(16, 1)
            print "IR turning ON"
        
            #Ir delay for resting 2 Seconds
            time.sleep(2) 

            # Assigning a variable so we can create a video .h264 file that contains the date and time as its name
            video = get_date + '_' +  get_time + '.h264'

            # Using the raspivid library to take a video
            cmd = 'raspivid -t 6000 -ex auto -w 1920 -h 1080 -o /media/usb0/' + video 
	    print 'cmd ' +cmd

            # If you find you have permission problems saving to other attached non-Naturebytes storage devices you can use this line to change the owner of the photo if required
            # perms = 'chown pi:pi /media/usb0/' + video
            # print 'perms ' +perms            

            # Log that we have just taken a video
            logging.info('About to take a video and save to the USB drive')
            call ([cmd], shell=True)
            # call ([perms], shell=True)
            
            # Log that a photo was taken successfully and state the file name so we know which one"
            logging.info('Video taken successfully %(show_video_name)s', { 'show_video_name': video })
            photo_location =  '/media/usb0/' + video                   

            #Sleep for 6  Seconds
            time.sleep(6)            
 
            #Turn off IR
            GPIO.output(16,0)
            print "IR turning OFF"

        else:

           # print "Waiting for a new PIR trigger to continue"
           logging.info('Waiting for a new PIR trigger to continue')

# END
