# Troubleshooting Vercel Deployment

## Common Errors and Solutions

### Error: FUNCTION_INVOCATION_FAILED (500 Internal Server Error)

This error means the serverless function crashed. Here's how to debug:

#### Step 1: Check Vercel Logs

1. Go to your Vercel project dashboard
2. Click on the failed deployment
3. Go to the "Functions" tab or "Logs" tab
4. Look for error messages

#### Step 2: Common Causes

**1. Missing Dependencies**
- Make sure `requirements.txt` includes all packages
- Check that `opencv-python`, `numpy`, `yt-dlp`, and `flask` are listed

**2. Import Errors**
- The app tries to import `youtube_averager.py`
- Make sure `youtube_averager.py` is in the root directory
- Check for any syntax errors in the file

**3. Template/Static File Issues**
- Make sure `templates/` and `static/` folders exist
- Check that `index.html` is in `templates/`
- Check that `style.css` and `script.js` are in `static/`

**4. File Path Issues**
- The app uses `/tmp/uploads` on Vercel
- Make sure the directory can be created (it should work automatically)

#### Step 3: Test the Health Endpoint

After deploying, try accessing:
```
https://your-app.vercel.app/health
```

This should return: `{"status": "ok", "message": "Server is running"}`

If this works, the Flask app is running but there might be an issue with the main route.

#### Step 4: Check Build Logs

1. In Vercel dashboard, go to your deployment
2. Click on "Build Logs"
3. Look for Python errors during the build process
4. Common issues:
   - Missing system dependencies (like `ffmpeg` for video processing)
   - Package installation failures
   - Python version mismatches

#### Step 5: Test Locally with Vercel

```bash
npm install -g vercel
vercel dev
```

This simulates the Vercel environment locally and can help identify issues.

### Error: Template Not Found

If you see "Template not found" errors:

1. Make sure `templates/index.html` exists
2. Check that the file is committed to git
3. Verify the `template_folder='templates'` setting in `app.py`

### Error: Static Files Not Loading

If CSS/JS files don't load:

1. Check that `static/style.css` and `static/script.js` exist
2. Make sure files are committed to git
3. Check browser console for 404 errors
4. Verify the `static_folder='static'` setting in `app.py`

### Error: Import Error for youtube_averager

If you see import errors:

1. Make sure `youtube_averager.py` is in the root directory
2. Check for syntax errors: `python -m py_compile youtube_averager.py`
3. Make sure all dependencies in `youtube_averager.py` are in `requirements.txt`

### Error: Timeout

If requests timeout:

- This is expected for longer videos
- Use frame interval options to process fewer frames
- Use max frames option to limit processing
- Consider upgrading to Pro/Enterprise for longer timeouts

## Debugging Steps

1. **Check Vercel Function Logs:**
   - Go to project → Deployments → Click deployment → Functions tab
   - Look for error messages

2. **Test Health Endpoint:**
   ```
   curl https://your-app.vercel.app/health
   ```

3. **Check Build Output:**
   - Look at build logs for installation errors
   - Verify all packages installed successfully

4. **Verify File Structure:**
   ```
   .
   ├── app.py
   ├── youtube_averager.py
   ├── requirements.txt
   ├── vercel.json
   ├── templates/
   │   └── index.html
   └── static/
       ├── style.css
       └── script.js
   ```

5. **Test Locally:**
   ```bash
   python app.py
   # Should start on http://localhost:5000
   ```

## Getting More Detailed Error Information

Add this to your `app.py` temporarily to see detailed errors:

```python
@app.errorhandler(Exception)
def handle_error(e):
    import traceback
    return jsonify({
        'error': str(e),
        'traceback': traceback.format_exc()
    }), 500
```

**Note:** Remove this in production as it exposes internal errors.

## Still Having Issues?

1. Check Vercel's official documentation: https://vercel.com/docs
2. Check Vercel community forums
3. Review the build and function logs carefully
4. Try deploying a minimal Flask app first to verify Vercel setup works

