/* 
  This file contains all the functions that are used by the camera feed or to interact with it.
  This includes taking a photo, toggling fullscreen, and changing the camera shutter mode.
*/
 
// Video feed fullscreen toggle
function toggleFullscreen() {
  const elem = document.querySelector(".main-box");
  let isFullScreen = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement;

  if (!isFullScreen) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  }
  isFullScreen = !isFullScreen;
}

/* Switching between Photo and Camera shutter modes */
const container = document.querySelector('#camera-type');
const photo = document.querySelector('#photo');
const video = document.querySelector('#video');
let startX = 0;
let isSwipe = false;
let currentIndex = 0;
video.addEventListener('touchend', (e) => {
  setActive(1);
});
photo.addEventListener('touchend', (e) => {
  setActive(0);
});

container.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
  isSwipe = false;
});
container.addEventListener('touchmove', (e) => {
  e.preventDefault(); // Prevent accidental scrolling
});
container.addEventListener('touchend', (e) => {
  let endX = e.changedTouches[0].clientX;
  let diff = startX - endX;

  if (diff > 30) {
    setActive(Math.min(1, currentIndex + 1)); // Swipe left → Next item
  } else if (diff < -30) {
    setActive(Math.max(0, currentIndex - 1)); // Swipe right → Previous item
  }
});
container.addEventListener('mousedown', (e) => {
  startX = e.clientX;
});
container.addEventListener('mouseup', (e) => {
  let endX = e.clientX;
  let diff = startX - endX;

  console.log(diff);

  if (diff > 10) {
    setActive(Math.min(1, currentIndex + 1)); // Swipe left → Next item
  } else if (diff < -10) {
    setActive(Math.max(0, currentIndex - 1)); // Swipe right → Previous item
  }
});

var shutterState = 0; // 0 for photo, 1 for video
// Sets the active shutter mode (Photo or Camera)
function setActive(index) {
  const modes = document.querySelectorAll('.mode');
  
  modes.forEach((mode, i) => {
      mode.classList.toggle('active', i === index);
  });
  
  const offset = (-index - 75) * index; 
  container.style.transform = `translateX(${offset}px)`;

  let shutter = document.getElementById('shutter');
  if (index == 0) {
    shutter.classList.add("photo-taking");
    shutter.classList.remove("video-taking");
    shutterState = 0;
  } else if (index == 1) {
    shutter.classList.add("video-taking");
    shutter.classList.remove("photo-taking");
    shutterState = 1;
  }
}
// Take the photo by clicking the shutter
function takePhoto() {
  if (shutterState == 1) { // Video mode
    alert("Video mode is not supported yet. Switch back to photo mode to take photos.");
    return;
  }

  let tooltip = document.getElementById('tooltip');
  if (tooltip) {
    tooltip.style.display = 'none';
  }

  // flash the camera feed
  const livestream = document.getElementById('livestream'); // this is the <img> tag that recieves the video feed
  livestream.style.opacity = 0.4;
  setTimeout(() => {
    livestream.style.opacity = 1;
  }, 90);

  // convert the img to canvas and download
  const canvas = document.createElement('canvas');

  // the width of livestream element can be different to the feed width
  let feedWidth = 1280;
  let feedHeight = 720;
  canvas.width = feedWidth;
  canvas.height = feedHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(livestream, 0, 0, canvas.width, canvas.height);

  canvas.toBlob((blob) => {
    const formData = new FormData();
    formData.append('file', blob, 'photo.png');

    fetch('http://127.0.0.1:5000/upload', {  // Change the endpoint accordingly
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      // request new recent images
      fetch('http://127.0.0.1:5000/recent-photos')
      .then(response => response.json())
      .then(data => {
        const galleryImagesOld = document.querySelectorAll(".gallery-image");
        images = Array.from(galleryImagesOld).map(img => img.src);

        galleryImagesOld.forEach((img, index) => {
          img.removeEventListener("click", () => openModal(index));
        });

        const gallery = document.getElementsByClassName('img-gallery')[0];
        // remove all gallery items
        while (gallery.firstChild) {
          gallery.removeChild(gallery.firstChild);
        }

        for (const image of data) {
          const item = document.createElement('div');
          item.classList.add('item');

          const head = document.createElement('div');
          head.classList.add('head');

          const img = document.createElement('img');
          img.src = image;
          img.classList.add('gallery-image');

          const zoom = document.createElement('div');
          zoom.classList.add('zoom-in');

          const zoomIcon = document.createElement('img');
          zoomIcon.src = '/static/assets/zoom.svg';
          zoomIcon.alt = '';
          zoomIcon.id = 'zoom-icon';

          zoom.appendChild(zoomIcon);
          head.appendChild(img);
          head.appendChild(zoom);

          const imgDetails = document.createElement('div');
          imgDetails.classList.add('img-details');

          const icon = document.createElement('div');
          icon.classList.add('icon');

          const iconItemDownload = document.createElement('div');
          iconItemDownload.classList.add('icon-item', 'download');
          iconItemDownload.onclick = () => downloadImage(image);

          const downloadIcon = document.createElement('img');
          downloadIcon.src = '/static/assets/download.svg';
          downloadIcon.alt = '';

          iconItemDownload.appendChild(downloadIcon);

          const iconItemDelete = document.createElement('div');
          iconItemDelete.classList.add('icon-item');
          iconItemDelete.id = 'delete-icon';
          iconItemDelete.onclick = () => deleteImage(image);

          const deleteIcon = document.createElement('img');
          deleteIcon.src = '/static/assets/delete.svg';
          deleteIcon.alt = '';

          iconItemDelete.appendChild(deleteIcon);

          icon.appendChild(iconItemDownload);
          icon.appendChild(iconItemDelete);

          imgDetails.appendChild(icon);

          item.appendChild(head);
          item.appendChild(imgDetails);

          gallery.appendChild(item);

        }
        const galleryImages = document.querySelectorAll(".gallery-image");
        images = Array.from(galleryImages).map(img => img.src);

        galleryImages.forEach((img, index) => {
          img.addEventListener("click", () => openModal(index));
        });
      })
    })
    .catch(error => console.error('Error:', error));
  }, 'image/png');
  
  /* 
  // Downloads the image
  const dataURL = canvas.toDataURL('image/png');

  const todayDateTimeString = new Date().toISOString().replace(/:/g, '-').split('.')[0];
  downloadImage(dataURL, `naturebytes-photo-${todayDateTimeString}.png`); */
}