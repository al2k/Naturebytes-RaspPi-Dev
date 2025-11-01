let mediaRecorder;
let recordedChunks = [];
let canvasStream;
let isRecording = false;
const frameRate = 15; // Match your backend’s frame rate (e.g., 30 FPS)

// Start or stop video recording
function takeVideo() {
  const livestream = document.getElementById('livestream'); // <img> element

  if (shutterState === 0) { // Photo mode
    alert("Switch to video mode to record videos.");
    return;
  }

  if (!isRecording) {
    startVideoRecording(livestream);
    document.getElementById("shutter").classList.add("recording");
  } else {
    stopVideoRecording();
    document.getElementById("shutter").classList.remove("recording");
  }
}

function startVideoRecording(livestream) {
  const canvas = document.createElement('canvas');
  let livestreamWidth = livestream.width;
  let livestreamHeight = livestream.height;

  if (livestreamWidth > 640) {
    livestreamHeight = (livestreamHeight / livestreamWidth) * 640;
    livestreamWidth = 640;
  }

  canvas.width = livestreamWidth;
  canvas.height = livestreamHeight;
  const ctx = canvas.getContext('2d');

  canvasStream = canvas.captureStream(frameRate);
  mediaRecorder = new MediaRecorder(canvasStream, { mimeType: 'video/webm; codecs=vp8' });

  recordedChunks = [];
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recordedChunks.push(event.data);
    }
  };

  mediaRecorder.onstop = () => {
    downloadVideo();
    isRecording = false;
    livestream.style.border = "none";
  };

  // Start recording first, then begin capturing frames
  mediaRecorder.start();
  isRecording = true;
  livestream.style.border = "2px solid red";

  captureFrames(livestream, ctx); // Start frame capture after recorder is active
}

function captureFrames(livestream, ctx) {
  if (!isRecording) return;

  // Draw the current <img> frame to the canvas
  ctx.drawImage(livestream, 0, 0, ctx.canvas.width, ctx.canvas.height);

  // Schedule the next frame at the specified frame rate
  setTimeout(() => captureFrames(livestream, ctx), 1000 / frameRate);
}

function stopVideoRecording() {
  if (isRecording && mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop();
  }
}

function downloadVideo() {
    const blob = new Blob(recordedChunks, { type: 'video/webm' });
    const url = URL.createObjectURL(blob);
  
    // Create a temporary link to trigger the download
    const link = document.createElement('a');
    link.href = url;
    link.download = 'recorded-video.webm'; // Filename for the downloaded video
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  
    // Clean up the URL object
    URL.revokeObjectURL(url);
  }