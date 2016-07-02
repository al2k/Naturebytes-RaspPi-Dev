==========================================
Testing your PIR (Passive Infrared sensor)
==========================================

Hi,

If you think you may have a problem with your PIR sensor then you can use our test script to help you troubleshoot the problem.

First of all, we should check that your sensor is connected to the Raspberry Pi.

1) Take a look at the PIR sensor and locate the three pins that say VCC, OUT and GND. These three pins should have a jumper cable (coloured wire) attached to each of them, and each wire should be plugged into the Raspberry Pi. Take a look in the Naturebytes instruction manual to make sure you have connected each wire to the correct GPIO (General Purpose Input Output) pins on the Raspberry Pi.

Does everything look correct? If it does, then let's continue.

2) Next, we can check if the PIR is detecting correctly by running a test script. A script is basically computer code in a file that has been programmed to understand when the sensor has been triggered. Let's run the test script and see if the PIR sensor is working. In the same folder as this readme.txt file that you are reading now you will see a file called "testpir.sh". Double click that and select the "Execute in Terminal" option from the popup screen to start.

3) You should see a message stating that your the pin is HIGH and so the PIR has been triggered, otherwise it will reset to LOW and wait to be triggered. If you don't see any activity and you are confident that it's correctly connected to the Raspberry Pi, then get in touch via the Naturebytes community and website and we'll help you troubleshoot further.

Kind regards,

The Naturebytes Team
