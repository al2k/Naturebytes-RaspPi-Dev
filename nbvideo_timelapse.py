#!/usr/bin/python
# Naturebytes Wildlife Cam Kit - Video timelapse] | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes

import os
import time
import datetime as dt
import logging
import sys
import getopt

from picamera2 import Picamera2
# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your 
# camera is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type 
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live.
# Alternatively, add -v to the launch to use verbosity mode

logging.basicConfig(format="%(asctime)s %(message)s", filename="naturebytes_camera_log", level=logging.DEBUG)
logging.info("Naturebytes Wildlife Cam Kit started up successfully")

# Set the resolution of the video you intend to capture.
#camera = Picamera2(resolution=(800, 600))

print("Starting up!")
sleep_time = 60
time.sleep(sleep_time)
print("Waiting %d seconds" % (sleep_time))


# Change the time.sleep value to delay the startup. The variable is in seconds, so it waits 60 seconds bef$

def main(argv):
    # Set default save location
    save_location = "/media/pi/"
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

    # Time defaults
    record_time = 5
    wait_time = 300

    # Take time lapse video series
    try:
        x = 1
        while True:
            filename = os.path.join(save_location, dt.datetime.now().strftime('%Y-%m-%d_%H.%M.%S.h264'))
            logging.info("Taking a video. This is video %d " % (x))
            printVerbose(verbose, msg=("Taking a video. This is video %d" % (x)))

            camera.start_recording(filename)
            camera.wait_recording(record_time)  # Record for 5 (record_time) seconds
            camera.stop_recording()
            logging.info("Video %(video_num)d completed", {"video_num": x})
            printVerbose(verbose, msg=("Video %d completed" % (x)))

            logging.info("Sleeping for %(wait_mins)d minutes and %(wait_secs)d seconds before recording again",
                         {"wait_mins": (wait_time / 60), "wait_secs": (wait_time % 60)})
            printVerbose(verbose, msg=("Sleeping for %d minutes and %d seconds before recording again" % (
            wait_time / 60, wait_time % 60)))
            time.sleep(wait_time)
            logging.info("Done. Preparing to record next video.")
            printVerbose(verbose, "Done. Preparing to record next video.")
            x += 1
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting program")
        sys.exit()
    except:
        print("Error detected. Exiting program")
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
    if (verbose): print("Log: " + msg)


if __name__ == "__main__":
    main(sys.argv[1:])
