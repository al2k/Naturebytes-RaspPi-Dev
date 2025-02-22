/* 
    This script is used to toggle the visibility of the content in the toggle-group.
    It is used by the "Testing & Settings" and "Help & Assembly Guides" sections on the right.
*/

document.addEventListener("DOMContentLoaded", function () {
  const toggleGroups = document.querySelectorAll(".toggle-group");

  toggleGroups.forEach(group => {
    const header = group.querySelector(".toggle-header");
    const content = group.querySelector(".toggle-content");

    group.addEventListener("click", function (e) {
      if (e.target !== header) {
        content.classList.add("show");
        header.classList.add("active");
      }
    });
    header.addEventListener("click", function (e) {
      e.stopPropagation();

      content.classList.toggle("show");
      header.classList.toggle("active");
    });
  });
});
