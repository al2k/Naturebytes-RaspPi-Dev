#!/usr/bin/python
# Naturebytes Wildlife Cam Kit | V1.01
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
import os
import csv
import time
import arrow
import logging


import RPi.GPIO as GPIO

from subprocess      import run
from multiprocessing import shared_memory

# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info('Naturebytes Wildlife Cam Kit started up successfully')

# Assigning a variable to the pins that we have connected the PIR to
SENSOR_PIN = 13
BATTERY_PIN = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BATTERY_PIN, GPIO.IN)

create = True
try:
    shm = shared_memory.SharedMemory('camera_control',create=create, size=1)
except FileExistsError:
    create = False
    shm = shared_memory.SharedMemory('camera_control',create=create, size=1)

# Default to taking still pictures
shm.buf[0]=1

def what_os():
    path = "/etc/os-release"
    with open(path) as stream:
        reader = csv.reader(stream, delimiter="=")
        os_release = dict(reader)
    return os_release


def take_photo(command, save_to, use_overlay, video):
    """
    Take a photo and if necessary add overlay
    :param command: str: command string to send
    :param use_overlay: bool: use an overlay or not
    :param video: bool: this is video if True else still
    :return: None
    """
    # Recording that a PIR trigger was detected and logging the battery level at this time
    logging.info('PIR trigger detected')
    # logging.info('Battery level is %(get_batt_level)s', { 'get_batt_level': batt_state })

    # Assigning a variable so we can create a photo JPG file that contains the date and time as its name
    now = arrow.now().format('YYYY-MM-DD_HH:mm:ss')

    if video:
        photo = now + '.h264'
    else:
        photo = now +'.jpg'

    # Using the raspistill library to take a photo and show that a photo has been taken in a small preview box on the desktop
    cmd = f'{command} -o {photo}'
    logging.info(f"cmd:{cmd}")

    # Log that we have just taking a photo"
    run(cmd.split())

    # Log that a photo was taken successfully and state the file name so we know which one"
    logging.info(f'Photo {photo} taken successfully')

    if os.path.exists(photo):
        if use_overlay:
            # Log that we are about to attempt to write the overlay text"
            logging.info('About to write the overlay text')
            overlay = "/usr/bin/convert " + photo + " "

            # Use ImageMagick to write text and meta data onto the photo.
            # overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + get_date + '" '" + get_time '" -gravity southeast -annotate +6+6 'Camera 1 " "'" + photo_location
            overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " \
                       + now + "' -gravity southeast -annotate +6+6 'Camera 1' " + photo

            # Log that we the text was added successfully"
            logging.info('Added the overlay text successfully')
            run(overlay.split())
            logging.info('Logo added successfully')

        run(["mv",f"./{photo}",f"{save_to}"])


def camera(save_to='./', use_overlay=False, video=False):

    # Starting with Bookworm the cammand name changed
    os_release = what_os()
    version = os_release.get('VERSION')
    if '12' in version:
        cam_command = 'rpicam-still' if not video else 'rpicam-vid -t 10s'
    else:
        cam_command = 'libcamera-still' if not video else 'libcamera-vid -t 10s'

    while True:

        # Map the state of the camera to our input pins (jumper cables connected to your PIR)
        if GPIO.input(SENSOR_PIN):
            if shm.buf[0]:
                video = False if shm.buf[0] == 1 else True
                take_photo(cam_command, save_to, use_overlay, video)
                time.sleep(10)


if __name__ == "__main__":
    import argparse
    args = argparse.ArgumentParser( prog='Capture camera images')
    save_to = '/usr/local/src/static/photos'
    overlay = True
    video = False

    args.add_argument('-s', '--save_to', type=str, default=save_to)
    args.add_argument('-o', '--overlay', action='store_true', default=False)
    args.add_argument('-v', '--video',   action='store_true', default=False)

    values = args.parse_args()
    camera(values.save_to, values.overlay, values.video)
