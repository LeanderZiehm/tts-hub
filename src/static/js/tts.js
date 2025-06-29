// tts.js - Handles all text-to-speech conversion functionality
console.log("tts.js 29.06.2025 v1");
// Import functions from history module
import { addToHistory, showAlert, downloadFile } from './history.js';

// DOM Elements
let textInput;
let engineSelect;
let convertBtn;
let progressContainer;
let progressBar;
let statusText;
let autoDownloadToggle;


// Initialize the TTS module
function initTTS() {
    // Get DOM references
    textInput = document.getElementById('textInput');
    engineSelect = document.getElementById('engineSelect');
    convertBtn = document.getElementById('convertBtn');
    progressContainer = document.getElementById('progressContainer');
    progressBar = document.getElementById('progressBar');
    statusText = document.getElementById('statusText');
    autoDownloadToggle = document.getElementById('autoDownloadToggle');
    console.log('▶︎ autoDownloadToggle is:', autoDownloadToggle);
console.log('▶︎ autoDownloadToggle.checked is:', autoDownloadToggle?.checked);

    
    // Load available TTS engines
    loadAndDisplayTTSEngines();
    
    // Add event listener for convert button
    convertBtn.addEventListener('click', convertTextToSpeech);
}

// Load and display available TTS engines
function loadAndDisplayTTSEngines() {
    fetch('/tts/engines')
        .then(response => response.json())
        .then(data => {
            data.forEach(engine => {
                const engineText = engine.charAt(0).toUpperCase() + engine.slice(1);
                const option = document.createElement('option');
                option.value = engine;
                option.textContent = engineText;
                engineSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error loading TTS engines:', error);
            showAlert('Failed to load TTS engines');
        });
}

// Convert text to speech
function convertTextToSpeech() {
    const text = textInput.value.trim();
    const engine = engineSelect.value;
    
    if (!text) {
        showAlert('Please enter some text to convert');
        return;
    }
    
    // Disable button and show progress
    convertBtn.disabled = true;
    progressContainer.style.display = 'block';
    progressBar.style.width = '20%';
    statusText.textContent = 'Sending request...';
    
    // Make API request
    fetch('/tts/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, engine })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to start conversion');
        }
        return response.json();
    })
    .then(data => {
        const jobId = data.job_id;
        progressBar.style.width = '40%';
        statusText.textContent = 'Processing...';
        
        // Poll for status
        pollConversionStatus(jobId, text, engine);
    })
    .catch(error => {
        console.error('Error starting conversion:', error);
        statusText.textContent = 'Error starting conversion';
        convertBtn.disabled = false;
        showAlert('Failed to start conversion');
        
        resetProgressBar();
    });
}

// Poll for conversion status
function pollConversionStatus(jobId, text, engine) {
    const checkStatus = setInterval(() => {
        fetch(`/tts/${jobId}/status`)
            .then(response => response.json())
            .then(statusData => {
                if (statusData.status === 'finished') {
                    clearInterval(checkStatus);
                    progressBar.style.width = '100%';
                    statusText.textContent = 'Conversion complete!';
                    //remove text from input area
                    textInput.value = '';
                
                    
                    // Add to history
                    addToHistory(jobId, text, engine);
                    
       
console.log('▶︎2 autoDownloadToggle is:', autoDownloadToggle);
console.log('▶︎2 autoDownloadToggle.checked is:', autoDownloadToggle?.checked);

   if (autoDownloadToggle.checked) {
    // console.log("toggle is checked")
                    // Auto download
                    setTimeout(() => {
                        console.log("download triggered through setTimeout")
                        downloadFile(jobId);
                        
                        // Reset UI
                        setTimeout(() => {
                            resetProgressBar();
                            convertBtn.disabled = false;
                        }, 1000);
                    }, 500);
                }
                    
                } else if (statusData.status === 'error') {
                    clearInterval(checkStatus);
                    progressBar.style.width = '100%';
                    statusText.textContent = 'Error: ' + statusData.detail;
                    convertBtn.disabled = false;
                    showAlert('Conversion failed: ' + statusData.detail);
                    
                    resetProgressBar();
                    
                } else {
                    // Still pending
                    progressBar.style.width = '70%';
                }
            })
            .catch(error => {
                clearInterval(checkStatus);
                console.error('Error checking status:', error);
                statusText.textContent = 'Error checking status';
                convertBtn.disabled = false;
                showAlert('Error checking conversion status');
                
                resetProgressBar();
            });
    }, 1000); // Check every second
}

// Reset progress bar
function resetProgressBar() {
    setTimeout(() => {
        progressContainer.style.display = 'none';
        progressBar.style.width = '0%';
    }, 3000);
}

// Export functions that will be used by other modules
export {
    initTTS
};