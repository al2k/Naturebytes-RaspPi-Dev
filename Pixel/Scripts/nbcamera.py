#!/usr/bin/env python
#
# Naturebytes Wildlife Cam Kit | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Usage: nbcamera.py -o <outputlocation>
# ======================================================================

import RPi.GPIO as GPIO
import time
from subprocess import call
from datetime import datetime
import logging
import getopt
import sys

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live

logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")

# Assigning a variable to the pins that we have connected the PIR to
sensor_pin = 13

# Command line defaults
verbose = False

# *** Legacy Kickstarter edition only *** 
# You may want to detect the battery status (low or high) if using a Powerboost. Change  'BATT' to True if doing this
BATT = False
if(BATT): low_batt_pin = 15

# Setting the GPIO (General Purpose Input Output) pins up so we can detect if they are HIGH or LOW (on or off)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
if(BATT): GPIO.setup(lowbattPin, GPIO.IN)

# Set default save location
saveLocation = "/media/usb0/"

def main(argv):
    # Set save location
    try:
        opts, args = getopt.getopt(argv, "hov:")
        for opt, arg in opts:
            if opt == "-h":
				printHelp()
				sys.exit()
            elif opt == "-o":
                saveLocation = arg
			elif opt == "-v"
				verbose = True
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    # Defining our default states so we can detect a change
    prev_state = False
    curr_state = False
	
	if(BATT):
		prev_batt_state = False
		curr_batt_state = False

    # Starting a loop
    while True:
        time.sleep(0.1)
        prev_state = curr_state
		if(BATT): prev_batt_state = curr_batt_state

        # Map the state of the camera to our input pins (jumper cables connected to your PIR)
        curr_state = GPIO.input(sensor_pin)
		if(BATT): curr_batt_state = GPIO.input(low_batt_pin)

        # Checking whether the state has changed
        if curr_state != prev_state:
			# Check if our new state is HIGH or LOW

            new_state = "HIGH" if curr_state else "LOW"
            new_batt_state = "HIGH" if curr_batt_state else "LOW"
            print "GPIO pin %s is %s" % (sensor_pin, new_state)
            print "GPIO pin %s is %s" % (low_batt_pin, new_batt_state)

            if curr_state: # State has changed to HIGH, so that must be a trigger from the PIR
                i = datetime.now() # Get current time
                get_date = i.strftime("%Y-%m-%d") # Get and format the date
                get_time = i.strftime("%H-%M-%S.%f") # Get and format the time
                
                # Recording that a PIR trigger was detected and logging the battery level at this time
                logging.info("PIR trigger detected")
				printVerbose("PIR trigger detected")
				if(BATT):
					logging.info("Battery level is %(get_batt_level)s", { "get_batt_level": batt_state })
					printVerbose("Battery level is %(get_batt_level)s", { "get_batt_level": batt_state })
                
                # Assigning a variable so we can create a photo JPG file that contains the date and time as its name
                photo_name = get_date + "_" +  get_time + ".jpg"

                # Using the raspistill library to take a photo. 
				# Show the photo that has been taken in a small preview box on the desktop by changing --nopreview to --preview
                cmd = "raspistill -t 300 -w 1920 -h 1440 --nopreview -o " + photo_name
                print "cmd " + cmd

                # Log that we have just taking a photo
                logging.info("About to take a photo and save to the USB drive")
				printVerbose("About to take a photo and save to the USB drive")
                call ([cmd], shell=True)
				
				# If you have permission problems saving to other attached non-Naturebytes storage devices,
				# uncomments the following three lines to change the owner of the photo
                # perms = 'chown pi:pi /media/usb0/' + photo
                # print 'perms ' + perms
				# call ([perms], shell=True)
				
                # Log that a photo was taken successfully and state the file name so we know which one"
                logging.info("Photo taken successfully %(show_photo_name)s", { "show_photo_name": photo_name })
				printVerbose("Photo taken successfully %(show_photo_name)s", { "show_photo_name": photo_name })
                photo_location = "/media/usb0/" + photo_name

            else:
               logging.info("Waiting for a new PIR trigger to continue")
			   printVerbose("Waiting for a new PIR trigger to continue")

def printHelp():
	options = """ 
			  usage: nbcamera.py [<options>] [--]
			  Options:
			  \t -o <outputlocation> \t specify output file location
			  \t -v                  \t be verbose
			  """
	print options
	
def printVerbose(str):
	if(verbose): print str
                			   		   
if __name__ == "main":
    main(sys.argv[1:])
