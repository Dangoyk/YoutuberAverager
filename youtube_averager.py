"""
YouTube Video Color Averager
Downloads a YouTube video and calculates the average color for each frame.
"""

import cv2
import numpy as np
import yt_dlp
import os
import sys
from pathlib import Path
import json
from typing import List, Tuple, Optional


class YouTubeColorAverager:
    def __init__(self, output_dir: str = "output"):
        """
        Initialize the YouTube Color Averager.
        
        Args:
            output_dir: Directory to save downloaded videos and results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.video_path = None
        self.frame_colors = []
        
    def download_video(self, url: str, quality: str = "best") -> str:
        """
        Download a YouTube video.
        
        Args:
            url: YouTube video URL
            quality: Video quality preference (best, worst, 720p, etc.)
            
        Returns:
            Path to downloaded video file
        """
        print(f"Downloading video from: {url}")
        
        # Configure yt-dlp options with better bot detection bypass
        ydl_opts = {
            'format': quality,
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            # Add headers to make it look like a real browser
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            # Additional options to help with bot detection
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
            # Retry on errors
            'retries': 3,
            'fragment_retries': 3,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info
                info = ydl.extract_info(url, download=True)
                video_title = info.get('title', 'video')
                
                # Find the downloaded file
                downloaded_files = list(self.output_dir.glob(f"{video_title}.*"))
                video_extensions = ['.mp4', '.webm', '.mkv', '.flv', '.avi']
                
                for file in downloaded_files:
                    if file.suffix.lower() in video_extensions:
                        self.video_path = str(file)
                        print(f"Video downloaded: {self.video_path}")
                        return self.video_path
                
                raise FileNotFoundError("Downloaded video file not found")
                
        except Exception as e:
            print(f"Error downloading video: {e}")
            raise
    
    def calculate_average_color(self, frame: np.ndarray) -> Tuple[int, int, int]:
        """
        Calculate the average RGB color of a frame.
        
        Args:
            frame: Video frame as numpy array (BGR format from OpenCV)
            
        Returns:
            Tuple of (R, G, B) average color values
        """
        # Convert BGR to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Calculate mean for each channel
        avg_color = np.mean(frame_rgb, axis=(0, 1))
        
        return tuple(map(int, avg_color))
    
    def process_video(self, video_path: Optional[str] = None, 
                     frame_interval: int = 1,
                     max_frames: Optional[int] = None) -> List[Tuple[int, int, int]]:
        """
        Process video and calculate average color for each frame.
        
        Args:
            video_path: Path to video file (uses self.video_path if None)
            frame_interval: Process every Nth frame (1 = all frames)
            max_frames: Maximum number of frames to process (None = all)
            
        Returns:
            List of average RGB colors for each processed frame
        """
        if video_path is None:
            video_path = self.video_path
        
        if video_path is None:
            raise ValueError("No video path provided")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"Processing video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        frame_count = 0
        processed_count = 0
        self.frame_colors = []
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"Video info: {total_frames} frames, {fps} FPS, {duration:.2f} seconds")
        print(f"Processing every {frame_interval} frame(s)...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame if it matches the interval
            if frame_count % frame_interval == 0:
                avg_color = self.calculate_average_color(frame)
                self.frame_colors.append(avg_color)
                processed_count += 1
                
                # Progress update
                if processed_count % 100 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"Processed {processed_count} frames ({progress:.1f}%)")
                
                # Check max frames limit
                if max_frames and processed_count >= max_frames:
                    break
            
            frame_count += 1
        
        cap.release()
        
        print(f"Processing complete! Analyzed {processed_count} frames.")
        return self.frame_colors
    
    def get_overall_average(self) -> Tuple[int, int, int]:
        """
        Calculate the overall average color across all frames.
        
        Returns:
            Tuple of (R, G, B) average color values
        """
        if not self.frame_colors:
            raise ValueError("No frame colors available. Process video first.")
        
        avg_r = np.mean([color[0] for color in self.frame_colors])
        avg_g = np.mean([color[1] for color in self.frame_colors])
        avg_b = np.mean([color[2] for color in self.frame_colors])
        
        return (int(avg_r), int(avg_g), int(avg_b))
    
    def save_results(self, filename: str = "color_averages.json"):
        """
        Save color averages to a JSON file.
        
        Args:
            filename: Output filename
        """
        if not self.frame_colors:
            raise ValueError("No frame colors to save")
        
        results = {
            "frame_colors": self.frame_colors,
            "overall_average": self.get_overall_average(),
            "total_frames": len(self.frame_colors)
        }
        
        output_path = self.output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {output_path}")
        return output_path
    
    def create_color_visualization(self, output_filename: str = "color_timeline.png",
                                  width: int = 1920, height: int = 100):
        """
        Create a visualization showing the color timeline.
        
        Args:
            output_filename: Output image filename
            width: Width of the visualization
            height: Height of each color bar
        """
        if not self.frame_colors:
            raise ValueError("No frame colors to visualize")
        
        # Create image with color bars
        num_frames = len(self.frame_colors)
        bar_width = max(1, width // num_frames)
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i, color in enumerate(self.frame_colors):
            x_start = i * bar_width
            x_end = min((i + 1) * bar_width, width)
            # OpenCV uses BGR, so reverse RGB to BGR
            img[:, x_start:x_end] = (color[2], color[1], color[0])
        
        output_path = self.output_dir / output_filename
        cv2.imwrite(str(output_path), img)
        print(f"Color visualization saved to: {output_path}")
        return output_path
    
    def print_summary(self):
        """Print a summary of the color analysis."""
        if not self.frame_colors:
            print("No data to summarize")
            return
        
        overall = self.get_overall_average()
        
        print("\n" + "="*50)
        print("COLOR ANALYSIS SUMMARY")
        print("="*50)
        print(f"Total frames analyzed: {len(self.frame_colors)}")
        print(f"Overall average color (RGB): {overall}")
        print(f"Overall average color (Hex): #{overall[0]:02x}{overall[1]:02x}{overall[2]:02x}")
        print("="*50 + "\n")


def main():
    """Main function to run the YouTube Color Averager."""
    if len(sys.argv) < 2:
        print("Usage: python youtube_averager.py <youtube_url> [options]")
        print("\nOptions:")
        print("  --frame-interval N    Process every Nth frame (default: 1)")
        print("  --max-frames N        Maximum frames to process (default: all)")
        print("  --quality QUALITY     Video quality (default: best)")
        print("  --output-dir DIR      Output directory (default: output)")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Parse arguments
    frame_interval = 1
    max_frames = None
    quality = "best"
    output_dir = "output"
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--frame-interval" and i + 1 < len(sys.argv):
            frame_interval = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--max-frames" and i + 1 < len(sys.argv):
            max_frames = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--quality" and i + 1 < len(sys.argv):
            quality = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output-dir" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    # Create averager instance
    averager = YouTubeColorAverager(output_dir=output_dir)
    
    try:
        # Download video
        video_path = averager.download_video(url, quality=quality)
        
        # Process video
        averager.process_video(frame_interval=frame_interval, max_frames=max_frames)
        
        # Print summary
        averager.print_summary()
        
        # Save results
        averager.save_results()
        
        # Create visualization
        averager.create_color_visualization()
        
        print("\nDone! Check the output directory for results.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

