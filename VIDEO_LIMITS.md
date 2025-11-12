# Video Length Limits

## Railway Free Tier Limits

### Processing Time
- **No strict timeout** - Railway doesn't kill long-running processes like Vercel does
- **$5 credit/month** - This is usually enough for testing
- Processing time depends on:
  - Video length
  - Number of frames processed
  - Video quality/resolution

### Practical Recommendations

**Short Videos (Best Results):**
- **Under 5 minutes**: Process all frames (frame interval = 1)
- **5-10 minutes**: Use frame interval of 2-5 (process every 2nd-5th frame)
- **10-30 minutes**: Use frame interval of 10-30 (process every 10th-30th frame)

**Long Videos:**
- **30+ minutes**: Use frame interval of 30-60
- **1+ hours**: Use frame interval of 60-120, or set max frames limit (e.g., 1000 frames)

### Memory Considerations

- Each frame requires memory to process
- Very long videos with all frames can use significant memory
- Railway free tier has memory limits

### Best Practices

1. **Start with frame sampling** - Use frame interval > 1 for videos over 5 minutes
2. **Use max frames** - Limit to 500-1000 frames for very long videos
3. **Lower quality** - Use 360p or 480p instead of "best" for faster processing
4. **Monitor Railway usage** - Check your credit usage in Railway dashboard

### Example Settings

**5-minute video at 30 FPS:**
- All frames: 9,000 frames - Takes ~5-10 minutes to process
- Every 10th frame: 900 frames - Takes ~1-2 minutes

**1-hour video at 30 FPS:**
- All frames: 108,000 frames - Would take hours, not recommended
- Every 60th frame: 1,800 frames - Takes ~10-15 minutes
- Max 1000 frames: Takes ~5-10 minutes

### Tips

- **Test with short videos first** to see how long processing takes
- **Use frame interval** to balance detail vs. processing time
- **Check Railway logs** to see actual processing time
- **Monitor credit usage** in Railway dashboard

## No Hard Limit

Unlike Vercel, Railway doesn't have a hard timeout. The main limits are:
- Your $5/month credit (free tier)
- Processing time (longer videos = more credit used)
- Memory usage (very long videos might hit memory limits)

For most use cases, videos under 30 minutes work well with appropriate frame sampling.

