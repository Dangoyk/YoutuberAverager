"""
Flask web application for YouTube Video Color Averager
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for
import os
import uuid
import threading
from pathlib import Path
import json

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Import after Flask app is created
YouTubeColorAverager = None
import_error_message = None

try:
    from youtube_averager import YouTubeColorAverager
    print("Successfully imported YouTubeColorAverager")
except ImportError as e:
    import_error_message = str(e)
    print(f"Error importing YouTubeColorAverager: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    import_error_message = str(e)
    print(f"Unexpected error importing YouTubeColorAverager: {e}")
    import traceback
    traceback.print_exc()

# Store processing status
processing_status = {}
processing_results = {}

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)


def process_video_task(task_id, url, frame_interval, max_frames, quality):
    """Background task to process video"""
    if YouTubeColorAverager is None:
        processing_status[task_id] = {
            'status': 'error',
            'progress': 0,
            'message': 'YouTubeColorAverager not available'
        }
        return
    
    try:
        processing_status[task_id] = {
            'status': 'downloading',
            'progress': 0,
            'message': 'Downloading video...'
        }
        
        # Create unique output directory for this task
        output_dir = UPLOAD_DIR / task_id
        output_dir.mkdir(exist_ok=True)
        
        # Create averager instance
        averager = YouTubeColorAverager(output_dir=str(output_dir))
        
        # Download video
        video_path = averager.download_video(url, quality=quality)
        
        processing_status[task_id] = {
            'status': 'processing',
            'progress': 25,
            'message': 'Processing frames...'
        }
        
        # Process video
        frame_colors = averager.process_video(
            frame_interval=frame_interval,
            max_frames=max_frames
        )
        
        processing_status[task_id] = {
            'status': 'finalizing',
            'progress': 90,
            'message': 'Generating results...'
        }
        
        # Get overall average
        overall_color = averager.get_overall_average()
        
        # Save results
        results_file = averager.save_results(f"{task_id}_results.json")
        
        # Create visualization
        viz_file = averager.create_color_visualization(f"{task_id}_timeline.png")
        
        # Create color video
        video_file = averager.create_color_video(f"{task_id}_timeline.mp4")
        
        # Store results
        processing_results[task_id] = {
            'overall_color': overall_color,
            'overall_color_hex': f"#{overall_color[0]:02x}{overall_color[1]:02x}{overall_color[2]:02x}",
            'total_frames': len(frame_colors),
            'timeline_image': f"{task_id}_timeline.png",
            'timeline_video': f"{task_id}_timeline.mp4",
            'results_file': f"{task_id}_results.json"
        }
        
        processing_status[task_id] = {
            'status': 'completed',
            'progress': 100,
            'message': 'Processing complete!'
        }
        
    except Exception as e:
        processing_status[task_id] = {
            'status': 'error',
            'progress': 0,
            'message': f'Error: {str(e)}'
        }


@app.route('/')
def index():
    """Main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {str(e)}", 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Server is running',
        'youtube_averager_available': YouTubeColorAverager is not None,
        'import_error': import_error_message if import_error_message else None
    })

@app.route('/favicon.ico')
def favicon():
    """Favicon endpoint to prevent 404 errors"""
    return '', 204  # No content

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    try:
        file_path = os.path.join(app.static_folder, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Set correct MIME types
        mimetype = None
        if filename.endswith('.css'):
            mimetype = 'text/css'
        elif filename.endswith('.js'):
            mimetype = 'application/javascript'
        
        return send_file(file_path, mimetype=mimetype)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_video():
    """API endpoint to start video processing"""
    try:
        if YouTubeColorAverager is None:
            error_msg = 'Video processing not available'
            if import_error_message:
                error_msg += f': {import_error_message}'
            return jsonify({'error': error_msg, 'import_error': import_error_message}), 503
        
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'YouTube URL is required'}), 400
        
        url = data['url']
        frame_interval = int(data.get('frame_interval', 1))
        
        # Handle max_frames - can be None, empty string, or number
        max_frames_value = data.get('max_frames')
        if max_frames_value is None or max_frames_value == '':
            max_frames = None
        else:
            try:
                max_frames = int(max_frames_value)
                if max_frames <= 0:
                    max_frames = None
            except (ValueError, TypeError):
                max_frames = None
        
        quality = data.get('quality', 'best')
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Start processing in background thread
        thread = threading.Thread(
            target=process_video_task,
            args=(task_id, url, frame_interval, max_frames, quality)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'task_id': task_id})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in /api/process: {e}")
        print(error_trace)
        return jsonify({'error': str(e), 'traceback': error_trace}), 500


@app.route('/api/status/<task_id>')
def get_status(task_id):
    """Get processing status"""
    if task_id not in processing_status:
        return jsonify({'error': 'Task not found'}), 404
    
    status = processing_status[task_id].copy()
    
    # If completed, include results
    if status['status'] == 'completed' and task_id in processing_results:
        status['results'] = processing_results[task_id]
    
    return jsonify(status)


@app.route('/api/download/<task_id>/<filename>')
def download_file(task_id, filename):
    """Download result files"""
    file_path = UPLOAD_DIR / task_id / filename
    
    if not file_path.exists():
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(str(file_path), as_attachment=True)


@app.route('/api/image/<task_id>/<filename>')
def get_image(task_id, filename):
    """Serve image files"""
    file_path = UPLOAD_DIR / task_id / filename
    
    if not file_path.exists():
        return jsonify({'error': 'Image not found'}), 404
    
    return send_file(str(file_path), mimetype='image/png')


# For Railway, it will auto-detect the Flask app
# For local development
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

