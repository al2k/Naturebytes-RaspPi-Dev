#!/usr/bin/env python
#
# Naturebytes Wildlife Cam Kit | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Usage: sudo python nbcamera_batt.py [<options>] [--]
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
# Alternatively, add -v to the launch to use verbosity mode

logging.basicConfig(format="%(asctime)s %(message)s",filename="naturebytes_camera_log",level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")

# Assigning a variable to the pins that we have connected the PIR to
sensor_pin = 13

# *** Legacy Kickstarter edition only *** 
# You may want to detect the battery status (low or high) if using a Powerboost. 
# Use this script if so, else use nbcamera.py
low_batt_pin = 15

# Setting the GPIO (General Purpose Input Output) pins up so we can detect if they are HIGH or LOW (on or off)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(low_batt_pin, GPIO.IN)

def main(argv):
    # Set default save location
    save_location = "/media/usb0/"
    # Command line defaults
    verbose = False
    logo = False

    # Set save location
    try:
        opts, args = getopt.getopt(argv, "ho:lv")
        for opt, arg in opts:
            if opt == "-h":
                printHelp()
                sys.exit()
            elif opt == "-l":
                logo = True
            elif opt == "-o": # Basic error checking
                save_location = arg.strip()
                save_location = save_location if save_location.startswith("/") else "/" + save_location
                save_location = save_location if save_location.endswith("/") else save_location + "/"
            elif opt == "-v":
                verbose = True
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    
    # Take images when PIR trigger HIGH
    try:
        # Defining our default states so we can detect a change
        prev_state = False
        curr_state = False
        
        # Define default battery states
        prev_batt_state = False
        curr_batt_state = False
        
        # Starting a loop
        while True:
            time.sleep(0.1)
            prev_state = curr_state
            prev_batt_state = curr_batt_state
            
            # Map the state of the camera to our input pins (jumper cables connected to your PIR)
            curr_state = GPIO.input(sensor_pin)
            curr_batt_state = GPIO.input(low_batt_pin)
            
            # Checking whether the state has changed
            if curr_state != prev_state:
                # Check if our new state is HIGH or LOW
                new_state = "HIGH" if curr_state else "LOW"
                print("GPIO pin %s is %s" % (sensor_pin, new_state))
                
                new_batt_state = "HIGH" if curr_batt_state else "LOW"
                print("GPIO pin %s is %s" % (low_batt_pin, new_batt_state))
                
                if curr_state: # State has changed to HIGH, so that must be a trigger from the PIR
                    i = datetime.now() # Get current time
                    get_date = i.strftime("%Y-%m-%d") # Get and format the date
                    get_time = i.strftime("%H-%M-%S.%f") # Get and format the time
                    batt_state = new_batt_state # Checking the current status of the battery
                    
                    # Recording that a PIR trigger was detected and logging the battery level at this time
                    logging.info("PIR trigger detected")
                    printVerbose(verbose, "PIR trigger detected")
                    
                    logging.info("Battery level is %(get_batt_level)s", { "get_batt_level": batt_state })
                    printVerbose(verbose, msg=("Battery level is %s" % (batt_state)))
                        
                    # Assigning a variable so we can create a photo JPG file that contains the date and time as its name
                    photo_name = get_date + "_" +  get_time + ".jpg"

                    # Using the raspistill library to take a photo. 
                    # Show the photo that has been taken in a small preview box on the desktop by changing --nopreview to --preview
                    cmd = "raspistill -t 300 -w 1920 -h 1440 --nopreview -o " + save_location + photo_name
                    print("cmd: " + cmd)
				
                    # If you have permission problems saving to other attached non-Naturebytes storage devices,
                    # uncomments the following three lines to change the owner of the photo
                    # perms = "chown pi:pi /media/usb0/" + photo_name
                    # print("perms: " + perms)
                    
                    # Log that we have just taking a photo
                    logging.info("About to take a photo and save to the USB drive")
                    printVerbose(verbose, "About to take a photo and save to the USB drive")
                    call ([cmd], shell=True)
                    # call ([perms], shell=True)
                    
                    if(logo):
                        # Use ImageMagick to write text and meta data onto the photo.
                        photo_location = save_location + photo_name

                        overlay = "/usr/bin/convert " + photo_location + " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + get_date + " " + get_time + "' -gravity southeast -annotate +6+6 'Camera 1' " + photo_location
                        call ([overlay], shell=True)
                        
                        # Log that we the text was added successfully"
                        logging.info("Added the overlay text successfully")
                        printVerbose(verbose, "Added the overlay text successfully")
                        
                        # Add a small Naturebytes logo to the top left of the photo. Note - you could change this to your own logo if you wanted.
                        logging.info("Adding the Naturebytes logo")
                        printVerbose(verbose, "Adding the Naturebytes logo")
                        overlay = "/usr/bin/convert " + photo_location + " /home/pi/Naturebytes/Scripts/naturebytes_logo_80.png -geometry +1+1 -composite " + photo_location
                        call ([overlay], shell=True)
    
                    # Log that a photo was taken successfully and state the file name so we know which one"
                    logging.info("Photo taken successfully %(show_photo_name)s", { "show_photo_name": photo_name })
                    printVerbose(verbose, msg=("Photo taken successfully %s" % (photo_name)))
            	else:
                    logging.info("Waiting for a new PIR trigger to continue")
                    printVerbose(verbose, "Waiting for a new PIR trigger to continue")
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting program")
        GPIO.cleanup()
        sys.exit()
    except:
        print("Error detected. Exiting program")
        GPIO.cleanup()
        sys.exit(2)

def printHelp():
    options = """ 
            usage: sudo python nbcamera_batt.py [<options>] [--]
            Options:
            \t -l                  \t Overlay Naturebytes logo onto captured image  
            \t -o <outputlocation> \t specify output file location
            \t -v                  \t be verbose - print log in terminal
            """
    print(options)

def printVerbose(verbose, msg):
    if(verbose): print("Log: " + msg)

if __name__ == "__main__":
    main(sys.argv[1:])