from picamera2 import Picamera2
from libcamera import controls

def main():
    picam2 = Picamera2()
    picam2.start(show_preview=False)
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous,
                         "AfSpeed": controls.AfSpeedEnum.Fast})

    picam2.start_and_capture_file("test.jpg")

if __name__ == "__main__":
    main()