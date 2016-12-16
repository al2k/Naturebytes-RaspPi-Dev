#!/bin/sh
# testcamera_withpir.sh
# This script kills any existing Python scripts that may be running and concentrates on testing the camera and PIR

sudo killall python
python testcamera_withpir.py

