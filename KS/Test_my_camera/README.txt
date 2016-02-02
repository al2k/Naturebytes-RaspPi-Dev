==========================================
Testing your Raspberry Pi camera
==========================================

Hi,

If you think you may have a problem with your camera then you can use our test script to help you troubleshoot the problem.

First of all, we should check that your camera is connected to the Raspberry Pi correctly. The camera is connected via the long, flat, flexible cable that has a blue strip on the end. Make sure that this is connected to the Raspberry Pi board by looking at the official Naturebytes instructions and checking that it is connected. Also make sure that is is connected well and not loose, or only half plugged in to the CSI connector on the Raspberry Pi.

If everything looks to be connected correctly, let's test that the camera is taking photos.

1) In the same folder as this readme.txt file you will see a file called "testcamera_withpir.sh". Double click that to start the test script. This script will attempt to take a photo when the PIR has been triggered. If you don't have a PIR or think that your PIR is faulty, then use the second script below.

2) Double click the file "testcamera.sh" to start the test script. This script will initialise camera and take a photo. The photo is the displayed as a preview (fullscreen) on your monitor so you can check that the lens is clean and that it's focused correctly.

Don't see any photos, or the camera doesn't seem to be working? Get in touch via the Naturebytes website and we'll help you to troubleshoot the issue further - naturebytes.org

Kind regards,

The Naturebytes Team
 
