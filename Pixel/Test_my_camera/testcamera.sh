#!/bin/sh
# testcamera.sh
# This script kills any existing Python scripts that may be running and concentrates on testing the camera

sudo killall python
python testcamera.py

