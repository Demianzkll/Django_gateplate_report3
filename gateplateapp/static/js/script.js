// Зона завантаження
const uploadArea = document.querySelector('#upload-area');
const fileInput = document.querySelector('#fileInput');
const previewSection = document.querySelector('#preview-section');
const previewImage = document.querySelector('#preview-image');

if (uploadArea && fileInput && previewSection && previewImage) {
  uploadArea.addEventListener('click', () => fileInput.click());

  fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
      const reader = new FileReader();
      reader.onload = e => {
        previewImage.src = e.target.result;
        previewSection.style.display = 'block';
      };
      reader.readAsDataURL(fileInput.files[0]);
    } else {
      previewSection.style.display = 'none';
    }
  });
}



const modal = document.querySelector("#imageModal");
const modalImg = document.querySelector("#modalImg");
const closeBtn = document.querySelector(".close-modal");

document.querySelectorAll(".zoomable-img").forEach(img => {
  img.addEventListener("click", () => {
    modal.style.display = "flex";
    modalImg.src = img.src;
    document.body.style.overflow = "hidden"; 
  });
});

closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
  document.body.style.overflow = "auto";
});

modal.addEventListener("click", e => {
  if (e.target === modal) {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
  }
});