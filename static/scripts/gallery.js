/* 
  This script is used to handle the gallery functionality.
  It allows the user to view images in a modal and navigate between them.
  It also allows the user to download and delete images/videos, and filter by type.
*/

let currentImageIndex = 0;
let images = [];

// Function to filter gallery items based on checkbox states
function filterGallery() {
  const showPhotos = document.getElementById('show-photos').checked;
  const showVideos = document.getElementById('show-videos').checked;
  const galleryItems = document.querySelectorAll('.item');

  galleryItems.forEach(item => {
    const isVideo = item.dataset.type === 'video';
    if ((showPhotos && !isVideo) || (showVideos && isVideo)) {
      item.style.display = 'block';
    } else {
      item.style.display = 'none';
    }
  });

  // Update modal images array based on visible items
  images = Array.from(document.querySelectorAll('.gallery-image'))
    .filter(img => img.closest('.item').style.display !== 'none')
    .map(img => img.src);
}

// Function to open the modal and display the clicked image
function openModal(index) {
  currentImageIndex = index;
  const modal = document.getElementById("imageModal");
  const modalImg = document.getElementById("modalImage");
  modal.style.display = "block";
  modalImg.src = images[currentImageIndex];
}

// Function to close the modal
function closeModal() {
  const modal = document.getElementById("imageModal");
  modal.style.display = "none";
}

// Function to navigate between images
function navigate(direction) {
  currentImageIndex += direction;
  if (currentImageIndex >= images.length) {
    currentImageIndex = 0;
  } else if (currentImageIndex < 0) {
    currentImageIndex = images.length - 1;
  }
  const modalImg = document.getElementById("modalImage");
  modalImg.src = images[currentImageIndex];
}

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
  const galleryImages = document.querySelectorAll(".gallery-image");
  images = Array.from(galleryImages).map(img => img.src);

  // Modal functionality
  galleryImages.forEach((img, index) => {
    img.addEventListener("click", () => openModal(index));
  });

  const modal = document.getElementById("imageModal");
  const closeBtn = document.querySelector(".close");
  closeBtn.addEventListener("click", closeModal);

  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeModal();
    }
  });

  // Select all functionality
  const selectAllCheckbox = document.getElementById('select-all');
  const imageCheckboxes = document.querySelectorAll('.image-select');

  selectAllCheckbox.addEventListener('change', function() {
    imageCheckboxes.forEach(checkbox => {
      const item = checkbox.closest('.item');
      if (item.style.display !== 'none') {
        checkbox.checked = this.checked;
      }
    });
  });

  // Filter functionality
  const showPhotosCheckbox = document.getElementById('show-photos');
  const showVideosCheckbox = document.getElementById('show-videos');
  
  showPhotosCheckbox.addEventListener('change', filterGallery);
  showVideosCheckbox.addEventListener('change', filterGallery);

  // Initial filter application
  filterGallery();
});

function bulkDownload() {
  const selectedImages = Array.from(document.querySelectorAll('.image-select:checked'))
    .map(checkbox => checkbox.getAttribute('data-image'));
  
  if (selectedImages.length === 0) {
    alert('Please select at least one item to download');
    return;
  }

  selectedImages.forEach((image, index) => {
    setTimeout(() => {
      downloadImage(image, `media_${index + 1}${image.includes('.mp4') ? '.mp4' : '.jpg'}`);
    }, index * 500);
  });
}

function bulkDelete() {
  const selectedImages = Array.from(document.querySelectorAll('.image-select:checked'))
    .map(checkbox => checkbox.getAttribute('data-image'));
  
  if (selectedImages.length === 0) {
    alert('Please select at least one item to delete');
    return;
  }

  if (!confirm(`Are you sure you want to delete ${selectedImages.length} item(s)? THIS ACTION IS IRREVERSIBLE!`)) {
    return;
  }

  fetch("/delete-images", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ images: selectedImages }),
  })
  .then((res) => {
    if (res.status === 204) {
      window.location.reload();
    }
  })
  .catch((err) => {
    console.error(err);
    alert('Error deleting items');
  });
}

function downloadImage(image, name) {
  const a = document.createElement("a");
  a.href = image;
  a.download = name || (image.includes('.mp4') ? 'video.mp4' : 'image.jpg');
  a.click();
}

function deleteImage(image) {
  if (!confirm("Are you sure you want to delete this item? THIS ACTION IS IRREVERSIBLE!")) {
    return;
  }

  fetch("/delete-image", {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: image }),
  })
  .then((res) => {
    if (res.status === 204) {
      window.location.reload();
    }
  })
  .catch((err) => {
    console.error(err);
  });
}