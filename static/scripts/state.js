/*
    This file is for keeping the state of the camera
    In certain cases the video feed should be hidden, including the shutter button.
*/

// 0 - Livestreaming feed
// 1 - Motion Capture
// 2 - Camera Off
const LIVESTREAMING = 0;
const MOTION_CAPTURE = 1;
const CAMERA_OFF = 2;


// 0 - Photo
// 1 - Video
const PHOTO = 0;
const VIDEO = 1;

var motionCaptureState = PHOTO;

var videoFeedDiv;
var motionCaptureDiv;
var turnedOffDiv;
var cameraActions;
var motionCaptureState;

document.addEventListener("DOMContentLoaded", function () {
    videoFeedDiv = document.getElementById("livestream");
    motionCaptureDiv = document.getElementById("motion-capture-placeholder");
    turnedOffDiv = document.getElementById("camera-off-placeholder");
    cameraActions = document.getElementById("camera-actions");
    motionCaptureState = document.getElementById("motion-capture-state");
    
    updateCameraState(currentState, true);
});

function updateCameraState(state, initial=false) {
    switch (state) {
        case LIVESTREAMING:
            videoFeedDiv.style.display = "block";
            motionCaptureDiv.style.display = "none";
            turnedOffDiv.style.display = "none";

            cameraActions.style.display = "block";
            motionCaptureState.style.display = "none";

            if (initial) break;
            fetch(routeWatchLive)
                .then(response => {
                    if (response.ok) {
                        console.log("Camera is now watching live");
                    } else {
                        console.log("Error: " + response.statusText);
                    }
                }).catch(error => {
                    console.log("Error: " + error);
                });
            break;
        case MOTION_CAPTURE:
            videoFeedDiv.style.display = "none";
            motionCaptureDiv.style.display = "flex";
            turnedOffDiv.style.display = "none";

            cameraActions.style.display = "none";
            motionCaptureState.style.display = "block";

            if (initial) break;
            
            console.log("Motion State: " + motionState);
            let route = routeCaptureImage;
            if (motionState == 2) {
                route = routeCaptureVideo;
            }

            fetch(route)
                .then(response => {
                    if (response.ok) {
                        console.log("Camera is now capturing motion");
                    } else {
                        console.log("Error: " + response.statusText);
                    }
                }).catch(error => {
                    console.log("Error: " + error);
                });
            break;
        case CAMERA_OFF:
            videoFeedDiv.style.display = "none";
            motionCaptureDiv.style.display = "none";
            turnedOffDiv.style.display = "flex";

            cameraActions.style.display = "none";
            motionCaptureState.style.display = "none";

            if (initial) break;
            fetch(routeStopCamera)
                .then(response => {
                    if (response.ok) {
                        console.log("Camera is now off");
                    } else {
                        console.log("Error: " + response.statusText);
                    }
                }).catch(error => {
                    console.log("Error: " + error);
                });
            break;
    }
}

function updateMotionState(state) {
    motionState = state;

    updateCameraState(MOTION_CAPTURE);
}