# Simple Vercel Deployment Guide

Follow these steps to deploy your YouTube Color Averager to Vercel.

## Prerequisites

- A GitHub account
- A Vercel account (free at [vercel.com](https://vercel.com))
- Your code pushed to a GitHub repository

## Step-by-Step Instructions

### Step 1: Push Your Code to GitHub

1. Create a new repository on GitHub
2. Push your code to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Website (Easiest)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Vercel will auto-detect Python settings
5. Click **"Deploy"**
6. Wait for deployment to complete (2-5 minutes)

#### Option B: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```
   - Follow the prompts
   - Press Enter to accept defaults

4. For production deployment:
   ```bash
   vercel --prod
   ```

### Step 3: Test Your Deployment

1. After deployment, Vercel will give you a URL like: `https://your-app.vercel.app`
2. Open the URL in your browser
3. Paste a YouTube video URL and test it!

## Important Notes

⚠️ **Timeout Limits:**
- **Free tier:** 10 seconds max per request
- **Pro tier:** 60 seconds max per request
- **Enterprise:** Up to 300 seconds (5 minutes)

**What this means:** Very short videos (under 30 seconds) will work best. Longer videos may timeout.

**Tips to avoid timeouts:**
- Use the "Frame Interval" option (e.g., set to 30 to process every 30th frame)
- Use the "Max Frames" option to limit processing
- Choose lower video quality (360p instead of best)

## Troubleshooting

### Deployment Fails

1. Check that `requirements.txt` includes all dependencies
2. Make sure `vercel.json` exists in your project root
3. Check Vercel build logs for specific errors

### App Times Out

- This is expected for longer videos on free/pro tiers
- Try shorter videos or use frame sampling options
- Consider upgrading to Enterprise for longer timeouts

### Static Files Not Loading

- Make sure `static/` folder is in your repository
- Check that `vercel.json` has the static file route configured

## File Structure

Your project should have:
```
.
├── app.py              # Main Flask app
├── youtube_averager.py # Core processing
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   └── index.html
└── static/            # CSS and JavaScript
    ├── style.css
    └── script.js
```

## That's It!

Your app should now be live on Vercel. Share the URL with others to use your YouTube Color Averager!

## Need Help?

- Check Vercel logs: Go to your project → Deployments → Click on a deployment → View Function Logs
- Vercel Docs: [vercel.com/docs](https://vercel.com/docs)
- See `VERCEL_DEPLOYMENT.md` for advanced configuration options

