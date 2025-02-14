// Initialize the carousel with pause disabled (ensure data-bs-pause="false" in HTML as well)
var carouselElement = document.getElementById('mediaCarousel');
var carouselInstance = new bootstrap.Carousel(carouselElement, { 
    interval: 5000,
    pause: false
});


// Load YouTube IFrame API asynchronously
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('youtube-player', {
        events: {
            'onStateChange': onPlayerStateChange
        }
    });
}

function onPlayerStateChange(event) {
    if (event.data === YT.PlayerState.PLAYING) {
        // Dispose the carousel to permanently stop auto-cycling
        carouselInstance.dispose();
        // Remove the auto-cycle attribute in case Bootstrap re-checks it
        carouselElement.removeAttribute('data-bs-ride');
    }
}
