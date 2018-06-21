# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:34:03 2018

@author: eimea
"""

#!/usr/bin/python
#
# Naturebytes Wildlife Cam Kit - Video by PIR | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Usage: sudo python nbvideo_pir.py [<options>] [--]
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

logging.basicConfig(format="%(asctime)s %(message)s", filename="naturebytes_camera_log", level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")

# Assigning a variable for the pin to which the PIR is connected
sensor_pin = 13

# Assigning a variable for the pin to which the IR LED arary is connected
ir_pin = 16

# Setting the GPIO (General Purpose Input Output) pins up so we can detect if they are HIGH or LOW (on or off)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # PIR sensor pin
GPIO.setup(ir_pin, GPIO.OUT, initial=0) # IR LED pin. Initial state is off

def main(argv):
    # Set default save location
    save_location = "/media/usb0/"
    # Command line defaults
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "ho:v")
        for opt, arg in opts:
            if opt == "-h":
                printHelp()
                sys.exit()
            elif opt == "-o":
                save_location = arg.strip()
                save_location = save_location if save_location.startswith("/") else "/" + save_location
                save_location = save_location if save_location.endswith("/") else save_location + "/"
            elif opt == "-v":
                verbose = True
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    try:
        # Defining our default states so we can detect a change
        prev_state = False
        curr_state = False
        
        # Starting a loop
        while True:
            time.sleep(0.1)
            prev_state = curr_state
        
            # Map the state of the camera to our input pins (jumper cables connected to your PIR)
            curr_state = GPIO.input(sensor_pin)

            # Checking that our state has changed
   
            if curr_state != prev_state:
                # Check if our new state is HIGH or LOW
                new_state = "HIGH" if curr_state else "LOW"
        
                print( "GPIO pin %s is %s" % (sensor_pin, new_state) )
                # print "Battery level detected via pin %s is %s" % (lowbattPin, newBattState)

                if curr_state:  # Our state has changed, so that must be a trigger from the PIR
                    i = datetime.now() # Get the time now
                    get_date = i.strftime("%Y-%m-%d") # Get and format the date
                    get_time = i.strftime("%H-%M-%S.%f") # Get and format the time

                    # Recording that a PIR trigger was detected
                    logging.info("PIR trigger detected")
                    printVerbose(verbose, "PIR trigger detected")
                
                    # Turn on IR
                    GPIO.output(ir_pin, 1)
                    logging.info("IR turning ON")
                    printVerbose(verbose, "IR turning ON")
                    time.sleep(2) # Wait 2 seconds to ensure IR is on
                    
                    # Assigning a variable so we can create a video .h264 file that contains the date and time as its name
                    video = get_date + "_" + get_time + ".h264"
                
                    # Using the raspivid library to take a video
                    cmd = "raspivid -t 6000 -ex auto -w 1920 -h 1080 -o " + save_location + video 
                    print("cmd " + cmd)
                      
                    # If you have permission problems saving to other attached non-Naturebytes storage devices,
                    # uncomments the following lines to change the owner of the photo
                    # perms = "chown pi:pi /media/usb0/" + video
                    # print "perms " + perms
                    
                    # Log that we have just taken a video
                    logging.info("About to take a video and save to the USB drive")
                    printVerbose(verbose, "About to take a video and save to the USB drive")
                    call ([cmd], shell=True)
                    # call ([perms], shell=True)
                
                    # Log that a photo was taken successfully and state the file name so we know which one"
                    logging.info("Video taken successfully %(show_video_name)s", { "show_video_name": video })
                    printVerbose(verbose, msg=("Video taken successfully %(show_video_name)s", { "show_video_name": video }))
                    # video_location = save_location + video
                
                    # Sleep for 6 Seconds
                    time.sleep(6)            
                
                    # Turn off IR
                    GPIO.output(ir_pin,0)
                    logging.info("IR turning OFF")
                    printVerbose(verbose, "IR turning OFF")

                else:
                    # print "Waiting for a new PIR trigger to continue"
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
# End of main

def printHelp():
    options = """ 
            usage: sudo python nbvideo_pir.py [<options>] [--]
            Options:
            \t -o <outputlocation> \t specify output file location
            \t -v                  \t be verbose - print log in terminal
            """
    print(options)

def printVerbose(verbose, msg):
    if(verbose): print("Log: " + msg)         

if __name__ == "__main__":
    main(sys.argv[1:])