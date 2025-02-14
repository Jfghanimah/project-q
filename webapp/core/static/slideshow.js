var images = ["static/game1.jpg", "static/game2.jpg", "static/game3.jpg", "static/game4.jpg"]; // Add more images to this array as needed
var currentImageIndex = 0;

function changeImage() {
    var container = document.querySelector(".slideshow-container");
    
    // Fade out the current image
    container.style.opacity = 0;
    
    // Wait for the transition to complete (500ms based on the CSS transition duration)
    setTimeout(function() {
        // Increment the index and loop back to the start if necessary
        currentImageIndex++;
        if (currentImageIndex >= images.length) {
            currentImageIndex = 0;
        }

        // Change the background image
        container.style.backgroundImage = "url('" + images[currentImageIndex] + "')";

        // Fade in the new image
        container.style.opacity = 1;
    }, 800); // Match this to the CSS transition duration
}

setInterval(changeImage, 4500); // Change the image every 5 seconds
