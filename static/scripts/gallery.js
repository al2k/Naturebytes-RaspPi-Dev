/* 
  This script is used to handle the gallery functionality.
  It allows the user to view images in a modal and navigate between them.
  It also allows the user to download the image.
*/

// Displaying the modal and navigating the images using arrows
let currentImageIndex = 0;
var images = [];

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

// Event listeners for opening and closing the modal
document.addEventListener("DOMContentLoaded", function () {
  const galleryImages = document.querySelectorAll(".gallery-image");
  images = Array.from(galleryImages).map(img => img.src);

  galleryImages.forEach((img, index) => {
    img.addEventListener("click", () => openModal(index));
  });

  const modal = document.getElementById("imageModal");
  const closeBtn = document.querySelector(".close");
  closeBtn.addEventListener("click", closeModal);

  // Close modal when clicking outside the image
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      closeModal();
    }
  });
});


// Function to download the image
function downloadImage(image, name="image.jpg") {
  const a = document.createElement("a");
  a.href = image;
  a.download = name;
  a.click();
}

// Function to delete the image
function deleteImage(image) {
  if (!confirm("Are you sure you want to delete this image? THIS ACTION IS IRREVERSIBLE!")) {
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
