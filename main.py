#!/usr/bin/python
# Naturebytes Wildlife Cam Kit | V1.01
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
import sys
import csv
import time
import arrow
import pathlib
import logging
import argparse

import RPi.GPIO as GPIO

from subprocess import call
from threading import Thread

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
logging.info('Naturebytes Wildlife Cam Kit started up successfully')

# Assigning a variable to the pins that we have connected the PIR to
SENSOR_PIN = 13
BATTERY_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def what_os():
    path = pathlib.Path("/etc/os-release")
    with open(path) as stream:
        reader = csv.reader(stream, delimiter="=")
        os_release = dict(reader)
    return os_release


def take_photo(command, save_to, use_overlay):
    """
    Take a photo and if necessary add overlay
    :param command: str: command string to send
    :param use_overlay: bool: use an overlay or not
    :return: None
    """
    # Recording that a PIR trigger was detected and logging the battery level at this time
    logging.info('PIR trigger detected')
    # logging.info('Battery level is %(get_batt_level)s', { 'get_batt_level': batt_state })

    # Assigning a variable so we can create a photo JPG file that contains the date and time as its name
    now = arrow.now().format('YYYY-MM-DD_HH:mm:ss')
    photo = now +'.jpg'

    # Using the raspistill library to take a photo and show that a photo has been taken in a small preview box on the desktop
    cmd = f'{command} --output ./{photo}'
    logging.info(f"cmd:{cmd}")

    # Log that we have just taking a photo"
    logging.info(f'About to take a photo {photo}')
    call([cmd], shell=True)


    # Log that a photo was taken successfully and state the file name so we know which one"
    logging.info('Photo taken successfully %(show_photo_name)s', {'show_photo_name': photo})
    photo_location =  save_to + photo

    if use_overlay:
        # Log that we are about to attempt to write the overlay text"
        logging.info('About to write the overlay text')

        overlay = "/usr/bin/convert " + photo_location + " "

        # Use ImageMagick to write text and meta data onto the photo.
        # overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + get_date + '" '" + get_time '" -gravity southeast -annotate +6+6 'Camera 1 " "'" + photo_location
        overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + now + "' -gravity southeast -annotate +6+6 'Camera 1' " + photo_location

        # Log that we the text was added successfully"
        logging.info('Added the overlay text successfully')
        call([overlay], shell=True)

        # Add a small Naturebytes logo to the top left of the photo. Note - you could change this to your own logo if you wanted.
        logging.info('Adding the Naturebytes logo')
        overlay = '/usr/bin/convert ' + photo_location + ' ./naturebytes_logo_80.png -geometry +1+1 -composite ' + photo_location
        call([overlay], shell=True)

        # Log that the logo was added successfully"
        logging.info('Logo added successfully')

def main(use_overlay=False, save_to='./'):
    prev_state = curr_state = 0

    # Starting with Bookworm the cammand name changed
    os_release = what_os()
    version = os_release.get('VERSION')
    if '12' in version:
        cam_command = 'rpicam-still'
    else:
        cam_command = 'libcamera-still'

    while True:
        time.sleep(0.1)
        prev_state = curr_state

        # Map the state of the camera to our input pins (jumper cables connected to your PIR)
        curr_state = GPIO.input(SENSOR_PIN)
        if not curr_state == prev_state:
            # About to check if our new state is HIGH or LOW

            state = "HIGH" if curr_state else "LOW"
            logging.info(f"GPIO {SENSOR_PIN} pin:{state}")
            # print "Battery level detected via pin %s is %s" % (lowbattPin, newBattState)

            if curr_state:  # Our state has changed, so that must be a trigger from the PIR
                task = Thread(target=take_photo, args=[cam_command, save_to, use_overlay])
                task.run()
            else:
                # print "Waiting for a new PIR trigger to continue"
                logging.info('Waiting for a new PIR trigger to continue')


if __name__ == "__main__":
    save_to = './'
    use_overlay = True
    if len(sys.argv)>1:
        save_to = sys.argv[1]
    try:
        use_overlay = False if sys.argv[2] == 'false' else True
    except IndexError:
        pass

    main(save_to, use_overlay)
