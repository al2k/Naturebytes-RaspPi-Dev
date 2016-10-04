#!/usr/bin/python
import RPi.GPIO as GPIO
import time

print ('Wave your hand in front of the camera / sensor to trigger your PIR')

# Check that your PIR "OUT" PIN is connected to the correct PIN on the Raspberry Pi. You can confirm this in the official Naturebytes Wildlife Cam Kit instructions
sensorPin = 13

# Set the GPIO (General Purpose Input Outout) PINs up and define that we want to read "sensorPin" that we assigned above
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensorPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define the state of the PIR i.e what was it doing previously, and what is it doing now - has it triggered?
prevState = False
currState = False

# Start a loop and check for a change in status. Tip - wave your hand in front of the sensor to trigger it.
while True:
    time.sleep(0.1)
    prevState = currState
    currState = GPIO.input(sensorPin)
    if currState != prevState:
        newState = "HIGH so it has been triggered" if currState else "LOW so it is waiting to trigger"
        print ("GPIO pin %s is %s" % (sensorPin, newState))

# END
