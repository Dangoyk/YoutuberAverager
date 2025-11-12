# Vercel Deployment Issues and Solutions

## Issue: 503 Service Unavailable on /api/process

### Symptom
- Getting 503 error when trying to process videos
- Health endpoint shows `youtube_averager_available: false`

### Root Cause
The `opencv-python` package requires system libraries that Vercel's serverless environment may not have:
- FFmpeg (for video processing)
- Various codec libraries
- System dependencies

### Solutions

#### Option 1: Check Health Endpoint
Visit: `https://your-app.vercel.app/health`

This will show:
- Whether YouTubeColorAverager imported successfully
- The actual import error message

#### Option 2: Check Vercel Build Logs
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the latest deployment
3. Check "Build Logs" for Python package installation errors
4. Look for errors related to:
   - `opencv-python` installation
   - Missing system libraries
   - Package compilation failures

#### Option 3: Use Headless OpenCV
If `opencv-python` fails, try `opencv-python-headless` which has fewer dependencies:

Update `requirements.txt`:
```
opencv-python-headless>=4.8.0
numpy>=1.24.0
yt-dlp>=2023.7.6
flask>=2.3.0
```

**Note:** Headless version might still have issues with video processing.

#### Option 4: Alternative Approach
Since Vercel has limitations for video processing, consider:

1. **Use a different platform:**
   - Railway (better for long-running processes)
   - Render (supports background workers)
   - Fly.io (container-based)

2. **Use external services:**
   - Process videos on a separate service
   - Use Vercel only for the frontend
   - Store results in a database/object storage

#### Option 5: Check Python Version
Vercel uses Python 3.9 by default. Make sure your code is compatible.

You can specify Python version in `runtime.txt`:
```
python-3.11
```

### Debugging Steps

1. **Check the health endpoint:**
   ```bash
   curl https://your-app.vercel.app/health
   ```

2. **Check function logs in Vercel:**
   - Dashboard → Project → Functions tab
   - Look for import errors or tracebacks

3. **Test locally with Vercel:**
   ```bash
   vercel dev
   ```
   This simulates the Vercel environment locally.

4. **Check if opencv-python installs:**
   The build logs should show if `opencv-python` installed successfully.

### Expected Error Messages

If you see errors like:
- `No module named 'cv2'` - opencv-python didn't install
- `libavcodec.so.XX: cannot open shared object file` - Missing system libraries
- `FFmpeg not found` - FFmpeg not available in environment

These indicate system library dependencies that Vercel might not provide.

### Quick Fix to Test

Try updating `requirements.txt` to use headless version:

```txt
opencv-python-headless>=4.8.0
numpy>=1.24.0
yt-dlp>=2023.7.6
flask>=2.3.0
```

Then redeploy and check `/health` endpoint again.

