#!/usr/bin/python
#
# Naturebytes Wildlife Cam Kit - Video by PIR | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes

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
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#config IR
GPIO.setup(ir_pin, GPIO.OUT, initial=0)

def main(argv):
    # Set default save location
    save_location = "/media/usb0/"
    # Command line defaults
    verbose = False

    try:
        opts, args = getopt.getopt(argv, "hov:")
        for opt, arg in opts:
            if opt == "-h":
                printHelp()
                sys.exit()
            elif opt == "-o":
                save_location = arg
            elif opt == "-v":
                verbose = True
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

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
                print("IR turning ON")
                
                # IR delay for resting 2 Seconds
                time.sleep(2) 
                
                # Assigning a variable so we can create a video .h264 file that contains the date and time as its name
                video = get_date + "_" + get_time + ".h264"
                
                # Using the raspivid library to take a video
                cmd = "raspivid -t 6000 -ex auto -w 1920 -h 1080 -o /media/usb0/" + video 
                print("cmd " + cmd)
                
                # Log that we have just taken a video
                logging.info("About to take a video and save to the USB drive")
                printVerbose(verbose, "About to take a video and save to the USB drive")
                call ([cmd], shell=True)
                
                # If you have permission problems saving to other attached non-Naturebytes storage devices,
                # uncomments the following three lines to change the owner of the photo
                # perms = "chown pi:pi /media/usb0/" + video
                # print "perms " + perms
                # call ([perms], shell=True)
                
                # Log that a photo was taken successfully and state the file name so we know which one"
                logging.info("Video taken successfully %(show_video_name)s", { "show_video_name": video })
                printVerbose(verbose, msg=("Video taken successfully %(show_video_name)s", { "show_video_name": video }) )
                # video_location = "/media/usb0/" + video
                
                # Sleep for 6  Seconds
                time.sleep(6)            
                
                # Turn off IR
                GPIO.output(ir_pin,0)
                print("IR turning OFF")

            else:
                # print "Waiting for a new PIR trigger to continue"
                logging.info("Waiting for a new PIR trigger to continue")
                printVerbose(verbose, )
# End of main

def printHelp():
    options = """ 
            usage: nbcamera.py [<options>] [--]
            Options:
            \t -o <outputlocation> \t specify output file location
            \t -v                  \t be verbose
            """
    print(options)

def printVerbose(verbose, msg):
    if(verbose): print(msg)         

if __name__ == "main":
    main(sys.argv[1:])