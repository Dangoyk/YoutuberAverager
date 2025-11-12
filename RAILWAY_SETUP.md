# Railway Deployment Guide

## Super Simple Setup

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Railway"
   git push origin main
   ```

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub (free)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Done! Railway auto-detects everything

## What Railway Does Automatically

✅ Detects Python from `requirements.txt`  
✅ Installs all dependencies  
✅ Detects Flask app from `app.py`  
✅ Runs with gunicorn (from `Procfile`)  
✅ Sets up environment variables  
✅ Gives you a URL  

## Files Railway Uses

- `requirements.txt` - Python dependencies
- `Procfile` - How to start the app
- `runtime.txt` - Python version (optional)
- `app.py` - Your Flask app

## Troubleshooting

### App won't start

1. Check Railway logs:
   - Dashboard → Your Project → Deployments
   - Click on deployment → View logs

2. Check `/health` endpoint:
   - Visit `https://your-app.railway.app/health`
   - Should return: `{"status": "ok", ...}`

### Dependencies not installing

- Check `requirements.txt` is correct
- Check Railway build logs for errors
- Make sure all packages are available on PyPI

### Port errors

- Railway sets `PORT` environment variable automatically
- The app uses `os.environ.get('PORT', 5000)` to handle this
- No manual configuration needed

## Free Tier Limits

- $5 credit per month
- Usually enough for testing and light usage
- Check usage in Railway dashboard

## That's It!

Railway is designed to be simple - just connect GitHub and deploy. No complex configuration needed!

