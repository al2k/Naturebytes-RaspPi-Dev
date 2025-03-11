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
  // Set up canvas to capture frames
  const canvas = document.createElement('canvas');
  canvas.width = 640; // Match your stream resolution (640x480)
  canvas.height = 480;
  const ctx = canvas.getContext('2d');

  // Create a MediaStream from the canvas
  canvasStream = canvas.captureStream(frameRate); // Creates a stream at the specified FPS
  mediaRecorder = new MediaRecorder(canvasStream, { mimeType: 'video/webm' });

  // Collect recorded data
  recordedChunks = [];
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recordedChunks.push(event.data);
    }
  };

  // When recording stops, save and upload
  mediaRecorder.onstop = () => {
    downloadVideo();
    isRecording = false;
    livestream.style.border = "none"; // Reset feedback
  };

  // Start recording
  mediaRecorder.start();
  isRecording = true;
  livestream.style.border = "2px solid red"; // Visual feedback

  // Capture frames from the <img> element
  captureFrames(livestream, ctx);
}

function captureFrames(livestream, ctx) {
  if (!isRecording) return;

  // Draw the current <img> frame to the canvas
  ctx.drawImage(livestream, 0, 0, ctx.canvas.width, ctx.canvas.height);

  // Schedule the next frame
  requestAnimationFrame(() => captureFrames(livestream, ctx));
  // Alternatively, use setTimeout for stricter timing:
  // setTimeout(() => captureFrames(livestream, ctx), 1000 / frameRate);
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