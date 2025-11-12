# Vercel Deployment Guide

## Important Limitations

⚠️ **Vercel has significant limitations for this application:**

1. **Timeout Limits:**
   - Free tier: 10 seconds
   - Pro tier: 60 seconds  
   - Enterprise: Up to 300 seconds (configured in vercel.json)

2. **File System:**
   - Read-only filesystem except `/tmp` directory
   - Files in `/tmp` are temporary and may be cleaned up

3. **Memory Limits:**
   - Free tier: 1024 MB
   - Pro tier: 3008 MB (configured in vercel.json)

4. **Stateless Functions:**
   - Serverless functions are stateless
   - In-memory storage (`processing_status`, `processing_results`) won't persist between requests
   - **This means background processing with threading won't work reliably**

## Recommended Solutions

### Option 1: Use External Storage (Recommended)
For production, you should use:
- **Database** (PostgreSQL, MongoDB) for storing task status
- **Object Storage** (AWS S3, Cloudflare R2) for storing video files and results
- **Queue System** (Redis, AWS SQS) for background job processing

### Option 2: Process Synchronously (Simple but Limited)
Modify the app to process videos synchronously within the request. This will work for short videos but will hit timeout limits for longer videos.

### Option 3: Use a Different Platform
Consider deploying to:
- **Railway** - Better for long-running processes
- **Render** - Supports background workers
- **Fly.io** - Good for containerized apps
- **AWS Lambda** - Similar to Vercel but with longer timeouts
- **Google Cloud Run** - Container-based, flexible timeouts

## Current Configuration

The current setup uses:
- `/tmp` directory for file storage (Vercel's writable directory)
- In-memory storage (will reset between function invocations)
- Background threading (may not complete before function timeout)

## Deployment Steps

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **For production:**
   ```bash
   vercel --prod
   ```

## Environment Variables

If you add external storage, set these in Vercel dashboard:
- Go to your project → Settings → Environment Variables
- Add variables like:
  - `DATABASE_URL`
  - `REDIS_URL`
  - `AWS_ACCESS_KEY_ID`
  - etc.

## Testing Locally with Vercel

```bash
vercel dev
```

This will simulate the Vercel environment locally.

## Notes

- The app is configured for 300-second timeout (Enterprise tier)
- Memory is set to 3008 MB (Pro tier)
- Files are stored in `/tmp/uploads` which is Vercel's writable directory
- Static files (CSS, JS) are served from the `/static` directory

## Recommended Architecture for Production

1. **Frontend:** Vercel (static files)
2. **API:** Vercel serverless functions (for quick endpoints)
3. **Processing:** Separate worker service (Railway, Render, etc.)
4. **Storage:** External database + object storage
5. **Queue:** Redis or similar for job management

This would require significant refactoring but would be production-ready.

