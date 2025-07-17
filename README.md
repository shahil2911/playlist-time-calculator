# YouTube Playlist Time Calculator

A web application that calculates the total duration of any YouTube playlist. Simply enter a YouTube playlist URL, and the app will tell you how long it would take to watch the entire playlist.

## Features

- Calculate the total duration of any YouTube playlist
- Show total number of videos in the playlist
- Display time it would take to watch at normal speed and at 1.5x speed
- Responsive UI that works on desktop and mobile devices
- Handle unavailable or private videos in playlists

## Technologies Used

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript
- APIs: YouTube Data API v3

## Local Development

### Prerequisites

- Python 3.9 or later
- A YouTube Data API key

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/PlaylistTimeCalculator.git
   cd PlaylistTimeCalculator
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   flask run
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment

This application is deployed on Render. To deploy your own version:

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Add the environment variable `YOUTUBE_API_KEY` with your API key
5. Deploy!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Flask](https://flask.palletsprojects.com/)
- [Font Awesome](https://fontawesome.com/) for icons
