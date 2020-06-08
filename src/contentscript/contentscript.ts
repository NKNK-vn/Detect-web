/**
 * Hide all image on web site
 * @param message Message from background or popup script
 */
const popupMessageHandler = (message) => {
    console.log('contentJS - incoming message:', message);
    if (message === 'hideImages') {
        let images = document.getElementsByTagName('img');
        for (let i = 0; i < images.length; i++) {
            if (images[i].width > 128) {
                images[i].classList.add('hideImageX');
            }
        }
    }
    if (message === 'showImages') {
        let images = document.getElementsByTagName('img');
        for (let i = 0; i < images.length; i++) {
            if (images[i].width > 128) {
                images[i].classList.remove('hideImageX');
            }
        }
    }
};

// Start scripts after setting up the connection to popup
chrome.runtime.onConnect.addListener((popupPort) => {
    // Listen for popup messages
    popupPort.onMessage.addListener(popupMessageHandler);
    // Set listener for disconnection (aka. popup closed)
    popupPort.onDisconnect.addListener(() => {
        console.log('in-content.js - disconnected from popup');
    });
});
