#!/bin/sh
# testpir.sh
# This script kills any existing Python scripts that may be running and concentrates on testing the PIR

sudo killall python
sudo python pirtest.py

