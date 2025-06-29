// history.js - Manages conversion history functionality by interacting with the backend API
console.log("history.js 29.06.2025 v1");
const FILE_NAME_TEXT_LENGTH = 80

// DOM Elements
let historyTable;
let historyTableBody;
let emptyHistory;
let alertBox;
let clearHistoryBtn;

// Initialize the history module
function initHistory() {
    // Get DOM references
    historyTable = document.getElementById('historyTable');
    historyTableBody = document.getElementById('historyTableBody');
    emptyHistory = document.getElementById('emptyHistory');
    alertBox = document.getElementById('alertBox');
    clearHistoryBtn = document.getElementById('clearHistoryBtn');
    
    // Add event listener for clear history button if it exists
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }
    
    // Load history from server
    fetchHistory();
}

// Fetch history from server
function fetchHistory() {
    fetch('/history')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch history');
            }
            return response.json();
        })
        .then(history => {
            updateHistoryDisplay(history);
        })
        .catch(error => {
            console.error('Error fetching history:', error);
            showAlert('Failed to load conversion history');
        });
}

// Add new item to history (only called when a new item is added from the server)
function addToHistory(historyItem) {
    // Update display immediately with new item
    fetchHistory();
}

// Update history display with provided history data
function updateHistoryDisplay(history) {
    if (!history || history.length === 0) {
        historyTable.style.display = 'none';
        emptyHistory.style.display = 'block';
        return;
    }
    
    historyTable.style.display = 'table';
    emptyHistory.style.display = 'none';
    
    // Clear existing rows
    historyTableBody.innerHTML = '';
    
    // Add rows for each conversion
    history.forEach((item) => {
        const row = document.createElement('tr');
        
        // console.log(item.text);
        // Truncate text for display
        const trimmedText = item.text.trim();
        const displayText = trimmedText.length > FILE_NAME_TEXT_LENGTH 
            ? trimmedText.substring(0, FILE_NAME_TEXT_LENGTH) + '...' 
            : trimmedText;
        
        // Format timestamp
        // console.log(item.timestamp);

        const timestamp = new Date(parseFloat(item.timestamp) * 1000).toLocaleString();

        row.innerHTML = `
            <td title="${trimmedText}">${displayText}</td>
            <td>${item.engine}</td>
            <td>${timestamp}</td>
            <td class="history-actions">
                <button class="download-btn" data-id="${item.jobId}" data-name="${displayText}">Download</button>
                <button class="delete-btn" data-id="${item.jobId}">Delete</button>
            </td>
        `;
        
        historyTableBody.appendChild(row);
    });
    
    // Add event listeners to buttons
// Add event listeners to buttons
document.querySelectorAll('.download-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const jobId = e.target.getAttribute('data-id');
        const fileName = e.target.getAttribute('data-name');
        downloadFile(jobId, fileName);

        // Change button style on click
        e.target.classList.add('clicked');
    });
});

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const jobId = e.target.getAttribute('data-id');
            deleteHistoryItem(jobId);
        });
    });
}

// Delete history item
function deleteHistoryItem(jobId) {
    // Make API call to delete the item on the server
    fetch(`/tts/${jobId}/delete`, {
        method: 'DELETE'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete item');
        }
        return response.json();
    })
    .then(data => {
        // Refresh history display
        fetchHistory();
        showAlert('Conversion deleted successfully', true);
    })
    .catch(error => {
        console.error('Error deleting file:', error);
        showAlert('Failed to delete conversion');
    });
}

// Clear all history
function clearHistory() {
    if (confirm('Are you sure you want to clear all conversion history?')) {
        fetch('/history', {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to clear history');
            }
            return response.json();
        })
        .then(data => {
            fetchHistory();
            showAlert('All history cleared successfully', true);
        })
        .catch(error => {
            console.error('Error clearing history:', error);
            showAlert('Failed to clear history');
        });
    }
}

// Download file
function downloadFile(jobId,fileName) {
    // console.log(`downloadFile was triggered with filename: ${fileName} and jobId: ${jobId} trace back the path where it was called from: ${new Error().stack}`);
    const link = document.createElement('a');
    link.href = `/tts/${jobId}/download`;
    link.download = `${fileName}.wav`; // Set a default filename
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Show alert message
function showAlert(message, isSuccess = false) {
    alertBox.textContent = message;
    alertBox.style.display = 'block';
    
    if (isSuccess) {
        alertBox.classList.add('success');
    } else {
        alertBox.classList.remove('success');
    }
    
    setTimeout(() => {
        alertBox.style.display = 'none';
    }, 5000);
}

// Export functions that will be used by other modules
export {
    initHistory,
    addToHistory,
    showAlert,
    downloadFile
};