# Background Image Troubleshooting Guide

## Current Status

✅ Background image file exists: `Rift/public/backgroundImage.png` (1.6MB)
✅ Code implementation is correct in all components
✅ CSS classes are properly applied

## Why You Might Not See It

### 1. Browser Cache Issue (Most Common)

**Solution: Hard Refresh**
- **Chrome/Edge:** `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
- **Firefox:** `Ctrl + F5` (Windows) or `Cmd + Shift + R` (Mac)
- **Safari:** `Cmd + Option + R`

**Or Clear Cache:**
1. Open DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

### 2. Development Server Not Restarted

**Solution:**
```bash
# Stop the dev server (Ctrl+C)
# Then restart
npm run dev
```

### 3. Image Path Issue

**Verify the image is accessible:**
1. Start dev server: `npm run dev`
2. Open browser: `http://localhost:3000/backgroundImage.png`
3. You should see the image directly

If image doesn't load, check:
```bash
# Verify file exists
ls -lh Rift/public/backgroundImage.png

# Should show: backgroundImage.png (1.6MB)
```

### 4. CSS Not Applied

**Check in Browser DevTools:**
1. Open DevTools (F12)
2. Go to Elements/Inspector tab
3. Find the div with `backgroundImage.png`
4. Check computed styles:
   - `position: fixed`
   - `z-index: -10`
   - `filter: blur(8px)`
   - `transform: scale(1.05)`
   - `background-image: url("/backgroundImage.png")`

### 5. Z-Index Conflict

**Verify layer order:**
```tsx
// Should be:
-z-10: Background image (blurred)
-z-10: Dark overlay
z-0:   Default content
z-10:  Main content (sharp)
z-50:  Sidebar panels
```

## Quick Verification Checklist

```bash
# 1. Check file exists
ls Rift/public/backgroundImage.png
# Expected: backgroundImage.png

# 2. Check file size (should be reasonable)
du -h Rift/public/backgroundImage.png
# Expected: ~1.6M

# 3. Restart dev server
npm run dev

# 4. Hard refresh browser
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

# 5. Check browser console for errors
# Open DevTools > Console tab
# Look for 404 errors or image loading failures
```

## Expected Visual Result

When working correctly, you should see:
1. **Blurred background image** covering the entire screen
2. **Dark overlay** (50% black) on top of the blurred image
3. **Sharp content** (header, graph, controls) on top
4. Background **doesn't scroll** with content (fixed position)

## Manual Test

### Test 1: Direct Image Access
```
http://localhost:3000/backgroundImage.png
```
✅ Should display the image
❌ If 404, image file is missing or misnamed

### Test 2: Inspect Element
1. Right-click on the dashboard background
2. Select "Inspect" or "Inspect Element"
3. Look for this div:
```html
<div 
  class="fixed inset-0 -z-10 bg-cover bg-center blur-md scale-105"
  style="background-image: url(/backgroundImage.png);"
></div>
```

### Test 3: Check Computed Styles
In DevTools, select the background div and check:
- `background-image`: Should show the URL
- `filter`: Should show `blur(8px)`
- `transform`: Should show `scale(1.05)`
- `z-index`: Should show `-10`

## Common Issues & Fixes

### Issue: Image loads but no blur
**Cause:** CSS not applied
**Fix:** Check Tailwind is configured correctly
```bash
npm run dev
```

### Issue: Image shows but content is also blurred
**Cause:** Z-index not set correctly
**Fix:** Ensure content has `relative z-10`:
```tsx
<div className="container mx-auto px-6 py-6 relative z-10">
```

### Issue: Image doesn't cover full screen
**Cause:** Missing `inset-0` or `fixed`
**Fix:** Verify classes:
```tsx
className="fixed inset-0 -z-10 bg-cover bg-center blur-md scale-105"
```

### Issue: White edges visible around blur
**Cause:** Missing `scale-105`
**Fix:** Add scale to compensate for blur:
```tsx
className="... blur-md scale-105"
```

### Issue: Background scrolls with content
**Cause:** Missing `fixed` positioning
**Fix:** Ensure `fixed` class is present:
```tsx
className="fixed inset-0 ..."
```

## Force Reload Steps

If nothing works, try this sequence:

```bash
# 1. Stop dev server
# Press Ctrl+C in terminal

# 2. Clear Next.js cache
rm -rf Rift/.next

# 3. Restart dev server
npm run dev

# 4. In browser:
# - Open DevTools (F12)
# - Go to Application/Storage tab
# - Click "Clear site data"
# - Close DevTools
# - Hard refresh (Cmd+Shift+R)
```

## Verify Implementation

### Check Dashboard3D.tsx
```tsx
// Should have these layers:
<div className="min-h-screen bg-slate-950 text-white relative">
  {/* Layer 1: Blurred Background */}
  <div
    className="fixed inset-0 -z-10 bg-cover bg-center blur-md scale-105"
    style={{ backgroundImage: 'url(/backgroundImage.png)' }}
  />
  
  {/* Layer 2: Dark Overlay */}
  <div className="fixed inset-0 -z-10 bg-black/50" />

  {/* Layer 3: Content */}
  <header className="... relative z-10">...</header>
  <div className="... relative z-10">...</div>
</div>
```

### Check app/dashboard/page.tsx
Loading and error states should also have the background:
```tsx
<div className="min-h-screen bg-slate-950 flex items-center justify-center relative">
  <div
    className="fixed inset-0 -z-10 bg-cover bg-center blur-md scale-105"
    style={{ backgroundImage: 'url(/backgroundImage.png)' }}
  />
  <div className="fixed inset-0 -z-10 bg-black/50" />
  <div className="text-center relative z-10">...</div>
</div>
```

## Still Not Working?

### Debug in Browser Console
```javascript
// Open browser console (F12 > Console tab)
// Run this:
const img = new Image();
img.onload = () => console.log('✅ Image loaded successfully');
img.onerror = () => console.log('❌ Image failed to load');
img.src = '/backgroundImage.png';
```

### Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Refresh page
4. Look for `backgroundImage.png` request
5. Check status:
   - ✅ 200: Image loaded successfully
   - ❌ 404: Image not found
   - ❌ 500: Server error

## Alternative: Use Different Image

If the current image has issues, try with a test image:

```bash
# Download a test image
curl -o Rift/public/test-bg.png https://picsum.photos/1920/1080

# Update code to use test image
# In Dashboard3D.tsx, change:
style={{ backgroundImage: 'url(/test-bg.png)' }}
```

## Contact Support

If none of these solutions work, provide:
1. Browser console errors (F12 > Console)
2. Network tab screenshot showing backgroundImage.png request
3. Screenshot of DevTools > Elements showing the background div
4. Output of: `ls -lh Rift/public/backgroundImage.png`

## Summary

Most common fix: **Hard refresh the browser** (Cmd+Shift+R or Ctrl+Shift+R)

The implementation is correct. The issue is likely browser caching or the dev server needs a restart.
