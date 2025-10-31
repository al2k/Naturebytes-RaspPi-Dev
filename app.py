import io
import os
import time
import math
import binascii

from flask import (
    Flask,
    Response,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify,
    redirect,
)

from threading          import Condition
from multiprocessing    import shared_memory
from picamera2          import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs  import FileOutput

# Local
from log import log


app = Flask("Image Gallery")
app.config["IMAGE_EXTS"] = [".png", ".jpg", ".jpeg", ".gif", ".tiff"]
app.config["VIDEO_EXTS"] = [".webm", ".mp4", ".avi", ".mov"]

"""
User a shared memory byte to control how the camera app takes pictures:
    0 - turn of pictures
    1 - still pictures
    2 - video clips of 10 seconds
    3 - live stream
"""
TURN_OFF_PICTURES = 0
STILL_PICTURES = 1
VIDEO_CLIPS = 2
LIVE_FEED = 3


try:
    shm = shared_memory.SharedMemory("camera_control", create=True, size=1)
    log.info("Creating shared memory camera_control")
except FileExistsError:
    shm = shared_memory.SharedMemory("camera_control", create=False, size=1)

# Default to taking still pictures
shm.buf[0] = STILL_PICTURES
log.info(f"SM:{shm.buf[0]}")


def encode(x):
    return binascii.hexlify(x.encode("utf-8")).decode()


def decode(x):
    return binascii.unhexlify(x.encode("utf-8")).decode()


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


def gen():
    """Video streaming generator function."""
    with Picamera2() as picam2:
        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
        output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(output))
        while not release:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n"
                    b"Content-Length: " + str(len(frame)).encode() + b"\r\n"
                    b"\r\n" + frame + b"\r\n"
                )


def get_photo_video_paths(limit=6, page=0):
    """
    @limit - number of images per page
    @page - current page number
    :return a list of image paths in the photo directory.
    """
    photo_dir = os.path.join(app.config.root_path, "static/photos/")
    media_paths = []
    for root, dirs, files in os.walk(photo_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config["IMAGE_EXTS"]):
                media_paths.append(
                    (
                        "image",
                        url_for("static", filename=f"photos/{file}", _external=True),
                    )
                )
            elif any(file.endswith(ext) for ext in app.config["VIDEO_EXTS"]):
                media_paths.append(
                    (
                        "video",
                        url_for("static", filename=f"photos/{file}", _external=True),
                    )
                )

    start = page * limit
    end = start + limit

    # sort
    media_paths.sort(
        key=lambda x: os.path.getmtime(os.path.join(photo_dir, x[1].split("/")[-1])),
        reverse=True,
    )

    return media_paths[start:end], len(media_paths)


@app.route("/pir-test")
def pir_test_route():
    pir_test()


@app.route("/")
def home():
    image_paths, _ = get_photo_video_paths(6, 0)

    if shm.buf[0] == TURN_OFF_PICTURES:
        camera_state = 2
    elif shm.buf[0] == STILL_PICTURES or shm.buf[0] == VIDEO_CLIPS:
        camera_state = 1
    else:
        camera_state = 0

    motion_state = 1
    if shm.buf[0] == STILL_PICTURES:
        motion_state = 1
    elif shm.buf[0] == VIDEO_CLIPS:
        motion_state = 2

    return render_template(
        "index.html",
        images=image_paths,
        camera_state=camera_state,
        motion_state=motion_state,
    )


@app.route("/gallery/", defaults={"page": 0})
@app.route("/gallery/<int:page>")
def gallery(page):
    per_page = 18
    image_paths, len_image_paths = get_photo_video_paths(per_page, page)
    return render_template(
        "gallery.html",
        images=image_paths,
        page=page,
        total_pages=math.ceil(len_image_paths / per_page),
        per_page=per_page,
        total_images=len_image_paths,
    )


@app.route("/cdn/<path:filepath>")
def download_file(filepath):
    dir, filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)


@app.route("/upload_file", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = "naturebytes-photo-" + time.strftime("%Y-%m-%dT%H-%M-%S") + ".png"
    file_path = os.path.join(app.config.root_path, "static/photos", filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully"}), 201


@app.route("/recent_photos")
def recent_photos():
    image_paths, _ = get_photo_video_paths(6, 0)
    return jsonify(image_paths)


@app.route("/delete-image", methods=["DELETE"])
def delete_image():
    data = request.get_json()
    image_path = data.get("image").split("photos/")[1]
    abs_path = os.path.join(
        app.config.root_path, os.path.join("static", "photos", image_path)
    )
    os.remove(abs_path)

    return "Success", 204


@app.route("/delete-images", methods=["DELETE"])
def delete_images():
    data = request.get_json()
    for image in data.get("images"):
        image_path = image.split("photos/")[1]
        abs_path = os.path.join(
            app.config.root_path, os.path.join("static", "photos", image_path)
        )
        os.remove(abs_path)

    return "Success", 204


import threading

camera = None
camera_lock = threading.Lock()


def initialize_camera():
    """Initialize the camera if not already initialized"""
    global camera
    with camera_lock:
        if camera is None:
            camera = Picamera2()
            camera_config = camera.create_preview_configuration(
                main={"size": (640, 480), "format": "RGB888"}
            )
            camera.configure(camera_config)


def release_camera():
    """Safely release the camera"""
    global camera, video_stream_active
    with camera_lock:
        if camera is not None:
            try:
                if video_stream_active:
                    camera.stop()
                    video_stream_active = False
                camera.close()
            except:
                pass  # Ignore errors during cleanup
            finally:
                camera = None


video_stream_active = False
camera_state = 0


def gen():
    """Video streaming generator function"""
    global camera, video_stream_active

    initialize_camera()

    with camera_lock:
        if not video_stream_active:
            camera.start()
            video_stream_active = True

    try:
        while camera_state == 0:  # Only stream when in livestreaming mode
            with camera_lock:
                if camera is None or not video_stream_active:
                    break

                stream = io.BytesIO()
                camera.capture_file(stream, format="jpeg")
                stream.seek(0)
                frame = stream.read()

            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    finally:
        # Clean up when streaming stops
        if camera_state != 0:
            release_camera()


release = False


def gen():
    """Video streaming generator function."""
    global release

    log.info("Video start recording")
    with Picamera2() as picam2:
        picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
        output = StreamingOutput()
        picam2.start_recording(JpegEncoder(), FileOutput(output))

        while not release:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n'
                    b'Content-Length: ' + str(len(frame)).encode() + b'\r\n'
                    b'\r\n' + frame + b'\r\n')

    log.info("Video stop recording")

@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    global release
    shm.buf[0] = LIVE_FEED
    release = False

    shm.buf[0] = TURN_OFF_PICTURES
    log.info(f"SM:{shm.buf[0]}")
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/capture_video")
def capture_video():
    """
    Start to capture short video instead of still images
    :return: Success
    """
    global release
    release = True
    shm.buf[0] = VIDEO_CLIPS
    log.info(f"SM:{shm.buf[0]}")
    return jsonify({"message": "Video capture started"}), 201


@app.route("/capture_image")
def capture_image():
    """
    Release video and let camera capture images
    :return:
    """
    global release
    release = True

    shm.buf[0] = STILL_PICTURES
    log.info(f"SM:{shm.buf[0]}")
    return "Success", 201


@app.route("/stop_camera")
def stop_camera():
    """
    Release the camera and stop all camera activity
    :return:
    """
    global release
    release = True

    shm.buf[0] = TURN_OFF_PICTURES
    log.info(f"SM:{shm.buf[0]}")
    return "Success", 201


"""
@app.route('/watch_live')
def watch_live():
    shm.buf[0] = TURN_OFF_PICTURES
    log.info(f"SM:{shm.buf[0]}")
    return jsonify({'message': 'Live stream started'}), 201
"""

if __name__ == "__main__":
    """
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    parser.add_argument('root_dir', help='Gallery root directory path')
    parser.add_argument('-l', '--listen', dest='host', default='0.0.0.0', \
                        help='address to listen on [0.0.0.0]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                        default=5000, help='port to listen on [5000]')
    args = parser.parse_args()
    """
    pass
    # app.config[]
    app.run(host="0.0.0.0", debug=True)
