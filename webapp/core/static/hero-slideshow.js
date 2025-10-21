document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector(".hero-slideshow-container");
  if (!container) return;

  // Read image URLs from the data attribute
  const images = JSON.parse(container.dataset.images || '[]');
  if (images.length === 0) return;

  let currentImageIndex = 0;

  // Preload images for smoother transitions
  images.forEach(src => {
    const img = new Image();
    img.src = src;
  });

  // Set the initial background image. This is the key to avoiding the clipping bug.
  container.style.backgroundImage = `radial-gradient(ellipse at center, rgba(18, 18, 18, 0.1) 0%, #181818 90%), url('${images[0]}')`;

  function cycleImages() {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    container.style.opacity = 0;
    setTimeout(() => {
      container.style.backgroundImage = `radial-gradient(ellipse at center, rgba(18, 18, 18, 0.1) 0%, #181818 90%), url('${images[currentImageIndex]}')`;
      container.style.opacity = 1;
    }, 500); // Corresponds to CSS transition duration
  }

  setInterval(cycleImages, 5000);
});