// Auto-hide flash messages after a few seconds
window.addEventListener('DOMContentLoaded', (event) => {
    const flashMessage = document.querySelector('.flash-message');
    if (flashMessage) {
        // Display the message (adding the 'show' class)
        flashMessage.classList.add('show');
        // Set a timeout to hide the message after 3 seconds
        setTimeout(() => {
            flashMessage.classList.remove('show');
            // Optionally, remove the element from the DOM
            setTimeout(() => flashMessage.remove(), 500);
        }, 2000);
    }
});