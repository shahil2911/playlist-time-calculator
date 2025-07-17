import os
import re
from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get YouTube API key from environment variable
API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_playlist_id_from_url(url):
    """Extract playlist ID from a YouTube URL."""
    # Regular expressions to match different YouTube playlist URL formats
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=([^&\s]+)',  # Standard playlist URL
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=[^&\s]+&list=([^&\s]+)',  # Watch URL with playlist
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/[^&\s]+\?list=([^&\s]+)'  # Short URL with playlist
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_playlist_info(playlist_id):
    """Get information about a YouTube playlist."""
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    try:
        # Get playlist details
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        
        if not playlist_response['items']:
            return None, "Playlist not found"
        
        playlist_title = playlist_response['items'][0]['snippet']['title']
        
        # Get all video IDs in the playlist
        video_ids = []
        next_page_token = None
        
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in playlist_items_response['items']:
                video_ids.append(item['contentDetails']['videoId'])
            
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
        
        # Get video durations
        total_seconds = 0
        video_count = 0
        unavailable_videos = 0
        
        # Process videos in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            videos_response = youtube.videos().list(
                part='contentDetails,snippet',
                id=','.join(batch_ids)
            ).execute()
            
            for video in videos_response.get('items', []):
                video_count += 1
                duration = video['contentDetails']['duration']
                # Convert ISO 8601 duration to seconds
                seconds = parse_duration(duration)
                total_seconds += seconds
        
        # Check if any videos were unavailable
        # Only count as unavailable if there's a significant difference
        unavailable_count = len(video_ids) - video_count
        unavailable_videos = unavailable_count if unavailable_count > 2 else 0
        
        # Calculate hours, minutes, seconds
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Format the time
        formatted_time = f"{int(hours)}:{int(minutes):02d}:{int(seconds):02d}"
        
        return {
            'playlist_title': playlist_title,
            'video_count': video_count,
            'unavailable_videos': unavailable_videos,
            'total_duration_seconds': total_seconds,
            'formatted_duration': formatted_time,
            'hours': int(hours),
            'minutes': int(minutes),
            'seconds': int(seconds)
        }, None
    
    except HttpError as e:
        error_message = f"An HTTP error occurred: {e.resp.status} {e.content}"
        return None, error_message
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return None, error_message

def parse_duration(duration_str):
    """Convert ISO 8601 duration string to seconds."""
    # Remove the 'PT' prefix
    duration_str = duration_str[2:]
    
    hours = 0
    minutes = 0
    seconds = 0
    
    # Find hours
    hour_pos = duration_str.find('H')
    if hour_pos != -1:
        hours = int(duration_str[:hour_pos])
        duration_str = duration_str[hour_pos + 1:]
    
    # Find minutes
    minute_pos = duration_str.find('M')
    if minute_pos != -1:
        minutes = int(duration_str[:minute_pos])
        duration_str = duration_str[minute_pos + 1:]
    
    # Find seconds
    second_pos = duration_str.find('S')
    if second_pos != -1:
        seconds = int(duration_str[:second_pos])
    
    return hours * 3600 + minutes * 60 + seconds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_playlist_time():
    data = request.get_json()
    playlist_url = data.get('playlist_url')
    
    if not playlist_url:
        return jsonify({'error': 'No playlist URL provided'}), 400
    
    playlist_id = get_playlist_id_from_url(playlist_url)
    if not playlist_id:
        return jsonify({'error': 'Invalid YouTube playlist URL'}), 400
    
    playlist_info, error = get_playlist_info(playlist_id)
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify(playlist_info)

if __name__ == '__main__':
    # Run with debug mode locally
    app.run(debug=True)
else:
    # Production settings when imported
    app.config['DEBUG'] = False
