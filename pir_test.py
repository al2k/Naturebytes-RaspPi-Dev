#!/usr/bin/python
import RPi.GPIO as GPIO
import time

print ('Wave your hand in front of the camera / sensor to trigger your PIR')

# Check that your PIR "OUT" PIN is connected to the correct PIN on the Raspberry Pi. You can confirm this in the official Naturebytes Wildlife Cam Kit instructions
sensor_pin = 13

# Set the GPIO (General Purpose Input Outout) PINs up and define that we want to read "sensorPin" that we assigned above
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def pir_test():
    # Define the state of the PIR i.e what was it doing previously, and what is it doing now - has it triggered?
    prev_state = curr_state = 0

    # Start a loop and check for a change in status. Tip - wave your hand in front of the sensor to trigger it.
    while True:
        time.sleep(0.1)
        prev_state = curr_state
        curr_state = GPIO.input(sensor_pin)
        if not curr_state == prev_state:
            state = "HIGH so it has been triggered" if curr_state else "LOW so it is waiting to trigger"
            print ("Pin %s is %s" % (sensor_pin, state))

if __name__ == "__main__":
    pir_test()