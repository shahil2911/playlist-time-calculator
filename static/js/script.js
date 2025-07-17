document.addEventListener('DOMContentLoaded', () => {
    // Make sure loading element is hidden on page load
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    // Ensure the error section is hidden on page load
    if (document.getElementById('unavailable-videos')) {
        document.getElementById('unavailable-videos').classList.add('hidden');
    }
    const form = document.getElementById('playlist-form');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const errorElement = document.getElementById('error');
    const errorMessageElement = document.getElementById('error-message');
    
    // Format duration in a human-readable way
    function formatDuration(hours, minutes, seconds) {
        let result = '';
        
        if (hours > 0) {
            result += `${hours} hour${hours !== 1 ? 's' : ''}`;
        }
        
        if (minutes > 0) {
            if (result) result += ' ';
            result += `${minutes} minute${minutes !== 1 ? 's' : ''}`;
        }
        
        if (seconds > 0 || (hours === 0 && minutes === 0)) {
            if (result) result += ' ';
            result += `${seconds} second${seconds !== 1 ? 's' : ''}`;
        }
        
        return result;
    }
    
    // Format duration for different watch speeds
    function formatWatchTime(totalSeconds) {
        const days = Math.floor(totalSeconds / (3600 * 24));
        const remainingSeconds = totalSeconds % (3600 * 24);
        const hours = Math.floor(remainingSeconds / 3600);
        const minutes = Math.floor((remainingSeconds % 3600) / 60);
        
        let result = '';
        
        if (days > 0) {
            result += `${days} day${days !== 1 ? 's' : ''}`;
            if (hours > 0 || minutes > 0) result += ' ';
        }
        
        if (hours > 0) {
            result += `${hours} hour${hours !== 1 ? 's' : ''}`;
            if (minutes > 0) result += ' ';
        }
        
        if (minutes > 0 || (days === 0 && hours === 0)) {
            result += `${minutes} minute${minutes !== 1 ? 's' : ''}`;
        }
        
        return result;
    }
    
    // Calculate time at different speeds
    function calculateSpeedTime(totalSeconds, speed) {
        return formatWatchTime(Math.round(totalSeconds / speed));
    }
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const urlInput = document.getElementById('playlist-url');
        const playlistUrl = urlInput.value.trim();
        
        if (!playlistUrl) {
            showError('Please enter a YouTube playlist URL');
            return;
        }
        
        // Hide results and error, show loading
        resultsElement.classList.add('hidden');
        errorElement.classList.add('hidden');
        loadingElement.classList.remove('hidden');
        
        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ playlist_url: playlistUrl })
            });
            
            const data = await response.json();
            
            // Hide loading
            loadingElement.classList.add('hidden');
            
            if (response.ok) {
                displayResults(data);
                // Results displayed successfully
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            loadingElement.classList.add('hidden');
            showError('Network error or server is not responding');
        }
    });
    
// Share functionality removed

function displayResults(data) {
        // Set playlist title
        document.getElementById('playlist-title').textContent = data.playlist_title;
        
        // Set formatted duration
        document.getElementById('formatted-duration').textContent = 
            formatDuration(data.hours, data.minutes, data.seconds);
        
        // Set video count
        document.getElementById('video-count').textContent = 
            `${data.video_count} video${data.video_count !== 1 ? 's' : ''}`;
        
        // Set watch time
        document.getElementById('watch-time').textContent = 
            formatWatchTime(data.total_duration_seconds);
        
        // Set 1.5x speed time
        document.getElementById('speed-time').textContent = 
            calculateSpeedTime(data.total_duration_seconds, 1.5);
        
        // Handle unavailable videos
        const unavailableVideosElement = document.getElementById('unavailable-videos');
        const unavailableCountElement = document.getElementById('unavailable-count');
        
        if (data.unavailable_videos > 0) {
            unavailableCountElement.textContent = data.unavailable_videos;
            unavailableVideosElement.classList.remove('hidden');
        } else {
            unavailableVideosElement.classList.add('hidden');
        }
        
        // Show results
        resultsElement.classList.remove('hidden');
    }
    
    function showError(message) {
        errorMessageElement.textContent = message;
        errorElement.classList.remove('hidden');
    }
});
