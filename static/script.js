let currentTaskId = null;
let statusCheckInterval = null;

document.getElementById('videoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const url = document.getElementById('youtubeUrl').value;
    const frameInterval = parseInt(document.getElementById('frameInterval').value) || 1;
    const maxFrames = document.getElementById('maxFrames').value || null;
    const quality = document.getElementById('quality').value;
    
    // Disable form
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitSpinner = document.getElementById('submitSpinner');
    
    submitBtn.disabled = true;
    submitText.textContent = 'Processing...';
    submitSpinner.style.display = 'inline-block';
    
    // Hide previous results/errors
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    // Show progress
    document.getElementById('progressSection').style.display = 'block';
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                frame_interval: frameInterval,
                max_frames: maxFrames ? parseInt(maxFrames) : null,
                quality: quality
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to start processing');
        }
        
        const data = await response.json();
        currentTaskId = data.task_id;
        
        // Start polling for status
        startStatusPolling();
        
    } catch (error) {
        showError(error.message);
        resetSubmitButton();
    }
});

function startStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    statusCheckInterval = setInterval(async () => {
        if (!currentTaskId) return;
        
        try {
            const response = await fetch(`/api/status/${currentTaskId}`);
            if (!response.ok) {
                throw new Error('Failed to get status');
            }
            
            const status = await response.json();
            updateProgress(status);
            
            if (status.status === 'completed') {
                clearInterval(statusCheckInterval);
                showResults(status.results);
                resetSubmitButton();
            } else if (status.status === 'error') {
                clearInterval(statusCheckInterval);
                showError(status.message);
                resetSubmitButton();
            }
        } catch (error) {
            clearInterval(statusCheckInterval);
            showError(error.message);
            resetSubmitButton();
        }
    }, 1000); // Poll every second
}

function updateProgress(status) {
    const progressBar = document.getElementById('progressBar');
    const progressMessage = document.getElementById('progressMessage');
    
    progressBar.style.width = `${status.progress}%`;
    progressMessage.textContent = status.message;
}

function showResults(results) {
    // Hide progress
    document.getElementById('progressSection').style.display = 'none';
    
    // Show results
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    // Update overall color
    const rgb = results.overall_color;
    const rgbString = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    
    document.getElementById('colorBox').style.backgroundColor = rgbString;
    document.getElementById('rgbValue').textContent = `(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    document.getElementById('hexValue').textContent = results.overall_color_hex;
    
    // Update frame count
    document.getElementById('frameCount').textContent = results.total_frames.toLocaleString();
    
    // Update timeline image
    const timelineImage = document.getElementById('timelineImage');
    timelineImage.src = `/api/image/${currentTaskId}/${results.timeline_image}`;
    
    // Update download links
    document.getElementById('downloadJson').href = `/api/download/${currentTaskId}/${results.results_file}`;
    document.getElementById('downloadImage').href = `/api/download/${currentTaskId}/${results.timeline_image}`;
}

function showError(message) {
    // Hide progress
    document.getElementById('progressSection').style.display = 'none';
    
    // Show error
    const errorSection = document.getElementById('errorSection');
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

function resetSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    const submitText = document.getElementById('submitText');
    const submitSpinner = document.getElementById('submitSpinner');
    
    submitBtn.disabled = false;
    submitText.textContent = 'Analyze Video';
    submitSpinner.style.display = 'none';
}

function resetForm() {
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('progressSection').style.display = 'none';
    currentTaskId = null;
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

