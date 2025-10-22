document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector(".hero-slideshow-container");
  if (!container) return;
  
  const images = JSON.parse(container.dataset.images || '[]');
  if (images.length === 0) return;

  const transitionDuration = parseInt(container.dataset.transitionDuration, 10) || 1500;
  const intervalTime = 6000;

  // Create two layers for cross-fading
  const layer1 = container.querySelector('.hero-slideshow-layer');
  const layer2 = layer1.cloneNode(true);
  container.appendChild(layer2);
  const layers = [layer1, layer2];

  // Apply transition duration from data attribute
  layers.forEach(layer => layer.style.transitionDuration = `${transitionDuration / 1000}s`);

  let currentImageIndex = 0;
  let currentLayerIndex = 0;

  // Preload images for smoother transitions
  images.forEach(src => {
    const img = new Image();
    img.src = src;
  });
  
  // Set up the initial state
  function setLayerImage(layer, imageIndex) {
    // The visual effects are now handled by the CSS overlay, so we just set the image.
    layer.style.backgroundImage = `url('${images[imageIndex]}')`;
  }
  
  setLayerImage(layers[0], currentImageIndex);
  layers[0].style.opacity = 1;
  
  function cycleImages() {
    // Determine next image and next layer
    currentImageIndex = (currentImageIndex + 1) % images.length;
    const nextLayerIndex = 1 - currentLayerIndex;
    
    // Set the next image on the hidden layer
    setLayerImage(layers[nextLayerIndex], currentImageIndex);
    
    // Fade out the current layer to reveal the new one underneath
    layers[currentLayerIndex].style.opacity = 0;
    layers[nextLayerIndex].style.opacity = 1;
    
    currentLayerIndex = nextLayerIndex;
  }

  setInterval(cycleImages, intervalTime);
});