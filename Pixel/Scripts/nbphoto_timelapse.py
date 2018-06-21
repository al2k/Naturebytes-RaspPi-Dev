#!/usr/bin/python
#
# Naturebytes Wildlife Cam Kit | V1.07 (Pixel)
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
#
# Usage sudo python nbphoto_timelapse.py [<options>] [--]
# ======================================================================

from time import sleep
from picamera import PiCamera
import getopt
import sys


camera = PiCamera()
# camera.start_preview()
sleep(2)

def main(argv):    
    # Set default save location
    save_location = "/media/usb0/"

    # Set save location
    try:
        opts, args = getopt.getopt(argv, "ho:v")
        for opt, arg in opts:
            if opt == "-h":
                printHelp()
                sys.exit()
            elif opt == "-o": # Basic error checking
                save_location = arg.strip()
                save_location = save_location if save_location.startswith("/") else "/" + save_location
                save_location = save_location if save_location.endswith("/") else save_location + "/"
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)

    # Take time lapse image series
    try:
        for filename in camera.capture_continuous(save_location + "img{counter:03d}_{timestamp:%Y-%m-%d-%H-%M}.jpg"):
            print("Captured %s" % filename)
            sleep(120) # wait 2 mins
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting program")
        sys.exit()
    except:
        print("Error detected. Exiting program")
        sys.exit(2)

def printHelp():
    options = """
            usage: sudo python nbcamera.py [<options>] [--]
            Options: 
            \t -o <outputlocation> \t specify output file location
            """
    print(options)

if __name__ == "__main__":
    main(sys.argv[1:])