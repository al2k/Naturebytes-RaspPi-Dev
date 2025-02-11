import io
import os
import binascii

from flask              import Flask, Response, request, render_template, send_from_directory
from picamera2          import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs  import FileOutput
from threading          import Condition
from multiprocessing    import shared_memory

app = Flask("Image Gallery")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]

"""
User a shared memory byte to control how the camera app takes pictures:
    0 - turn of pictures 
    1 - still pictures
    2 - video clips of 10 seconds
"""
create = True
try:
    shm = shared_memory.SharedMemory('camera_control',create=create, size=1)
except FileExistsError:
    create = False
    shm = shared_memory.SharedMemory('camera_control',create=create, size=1)

# Default to taking still pictures
shm.buf[0]=1


def encode(x):
    return binascii.hexlify(x.encode('utf-8')).decode()


def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

@app.route('/')
def home():
    photo_dir = os.path.join(app.config.root_path, "static/photos/")
    image_paths = []
    for root,dirs,files in os.walk(photo_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                #image_paths.append(encode(os.path.join(root,file)))
                image_paths.append(os.path.join('static/photos',file))
    return render_template('index.html', images=image_paths)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir,filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)


def gen():
    """Video streaming generator function."""
    with Picamera2() as picam2:
        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
        output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                       b'\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture_video')
def capture_video():
    """
    Start to capture short video instead of still images
    :return: Success
    """
    shm.buf[0] = 2
    return "Success", 201


@app.route('/capture_image')
def capture_image():
    shm.buf[0] = 1
    return "Success", 201


@app.route('/stop_camera')
def stop_camera():
    shm.buf[0] = 0
    return "Success", 201


@app.route('/watch_live')
def watch_live():
    print("Watch Live")
    return "Success", 201


if __name__=="__main__":
    '''
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    parser.add_argument('root_dir', help='Gallery root directory path')
    parser.add_argument('-l', '--listen', dest='host', default='0.0.0.0', \
                        help='address to listen on [0.0.0.0]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                        default=5000, help='port to listen on [5000]')
    args = parser.parse_args()
    '''
    #app.config[]
    app.run(host='0.0.0.0', debug=True)