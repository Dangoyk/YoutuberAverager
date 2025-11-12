# YouTube Video Color Averager

A web application that downloads YouTube videos and calculates the average color for each frame, as well as the overall average color for the entire video. Available as both a web interface and a command-line tool.

## Features

- 🌐 **Web Interface**: Beautiful, modern web UI for easy use
- 📥 Download YouTube videos automatically
- 🎨 Extract and analyze every frame (or sample frames)
- 🎯 Calculate average RGB color for each frame
- 📊 Calculate overall average color for the entire video
- 📈 Generate color timeline visualization
- 💾 Export results to JSON
- 📱 Responsive design that works on all devices

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Web Application Usage

### Starting the Web Server

```bash
python app.py
```

The web application will start on `http://localhost:5000`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Paste a YouTube video URL
3. Configure options (optional):
   - **Frame Interval**: Process every Nth frame (1 = all frames)
   - **Max Frames**: Limit the number of frames to process
   - **Video Quality**: Choose video quality (best, 720p, 480p, etc.)
4. Click "Analyze Video"
5. Watch the progress bar as your video is processed
6. View results including:
   - Overall average color (RGB and Hex)
   - Color timeline visualization
   - Video statistics
   - Download options for JSON and image files

## Command-Line Usage

### Basic Usage

```bash
python youtube_averager.py <youtube_url>
```

Example:
```bash
python youtube_averager.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Advanced Options

```bash
python youtube_averager.py <youtube_url> [options]
```

Options:
- `--frame-interval N`: Process every Nth frame (default: 1, processes all frames)
  - Example: `--frame-interval 30` processes every 30th frame (useful for long videos)
- `--max-frames N`: Maximum number of frames to process (default: all)
  - Example: `--max-frames 1000` processes only the first 1000 frames
- `--quality QUALITY`: Video quality preference (default: best)
  - Options: best, worst, 720p, 480p, etc.
- `--output-dir DIR`: Output directory (default: output)

### Example Commands

```bash
# Process all frames of a video
python youtube_averager.py https://www.youtube.com/watch?v=VIDEO_ID

# Process every 30th frame (faster for long videos)
python youtube_averager.py https://www.youtube.com/watch?v=VIDEO_ID --frame-interval 30

# Process only first 500 frames
python youtube_averager.py https://www.youtube.com/watch?v=VIDEO_ID --max-frames 500

# Download in 720p quality
python youtube_averager.py https://www.youtube.com/watch?v=VIDEO_ID --quality 720p
```

## Output

The tool creates output files containing:

1. **Downloaded video file**: The original video file (in `uploads/` for web app, `output/` for CLI)
2. **color_averages.json**: JSON file with:
   - Array of average RGB colors for each frame
   - Overall average color for the entire video
   - Total number of frames analyzed
3. **color_timeline.png**: A visualization showing the color progression throughout the video

## Programmatic Usage

You can also use the `YouTubeColorAverager` class in your own Python scripts:

```python
from youtube_averager import YouTubeColorAverager

# Create instance
averager = YouTubeColorAverager(output_dir="my_output")

# Download video
averager.download_video("https://www.youtube.com/watch?v=VIDEO_ID")

# Process all frames
averager.process_video()

# Get overall average color
overall_color = averager.get_overall_average()
print(f"Overall average RGB: {overall_color}")

# Save results
averager.save_results("my_results.json")

# Create visualization
averager.create_color_visualization("my_timeline.png")
```

## How It Works

1. **Download**: Uses `yt-dlp` to download the YouTube video
2. **Frame Extraction**: Uses OpenCV to extract frames from the video
3. **Color Calculation**: For each frame, calculates the mean RGB values across all pixels
4. **Overall Average**: Calculates the mean of all frame averages
5. **Visualization**: Creates a horizontal color bar showing the color progression

## Notes

- Processing all frames of a long video can take time. Use `--frame-interval` to sample frames for faster processing.
- The downloaded video is saved in the output directory and can be deleted after processing if desired.
- Video quality affects processing time and file size.

## Project Structure

```
.
├── app.py                 # Flask web application
├── youtube_averager.py    # Core processing class (can be used standalone)
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── runtime.txt           # Python version
├── templates/
│   └── index.html        # Web interface HTML
├── static/
│   ├── style.css         # Web interface styles
│   └── script.js         # Web interface JavaScript
└── README.md             # This file
```

## Requirements

- Python 3.8+
- opencv-python
- numpy
- yt-dlp
- flask (for web interface)

## Notes

- Processing all frames of a long video can take time. Use frame interval options to sample frames for faster processing.
- The downloaded video is saved in the uploads directory (web app) or output directory (CLI) and can be deleted after processing if desired.
- Video quality affects processing time and file size.
- The web application runs on `localhost:5000` by default. To make it accessible on your network, change `host='0.0.0.0'` in `app.py`.

## Railway Deployment (Recommended)

### Quick Start

Railway is the easiest way to deploy this app - it auto-detects Python and Flask!

1. **Push your code to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Ready for Railway"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub (free)
   - Click **"New Project"** → **"Deploy from GitHub repo"**
   - Select your repository
   - Railway auto-detects Python and deploys!

3. **That's it!** Railway will:
   - Install dependencies from `requirements.txt`
   - Start your Flask app
   - Give you a URL like `your-app.railway.app`

### Railway Benefits

✅ **No configuration needed** - Railway auto-detects everything  
✅ **Better for long-running tasks** - No strict timeout limits  
✅ **Free tier available** - $5 credit/month (usually enough for testing)  
✅ **Simple deployment** - Just connect GitHub and deploy  

### Local Development

```bash
python app.py
```

The app will run on `http://localhost:5000`

## License

This project is open source and available for personal and educational use.

