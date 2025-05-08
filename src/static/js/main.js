// main.js - Main script that imports modules and initializes the application

// Import modules
import { initHistory } from './history.js';
import { initTTS } from './tts.js';

// Initialize the application
function initApp() {
    // Initialize modules
    initHistory();
    initTTS();
}

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', initApp);