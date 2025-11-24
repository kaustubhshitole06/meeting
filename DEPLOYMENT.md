# Deployment Guide for Render

## Prerequisites

1. A GitHub account
2. A Render account (sign up at https://render.com)
3. Git installed on your machine

## Step-by-Step Deployment

### 1. Initialize Git Repository (if not already done)

```bash
cd c:\Users\User\Desktop\Phaze_AI_root\meeting
git init
git add .
git commit -m "Initial commit for Render deployment"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "meeting-assistant")
3. Don't initialize with README (you already have one)
4. Copy the repository URL

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Deploy on Render

#### Option A: Blueprint (Automatic - Recommended)

1. Go to https://dashboard.render.com/
2. Click **"New"** → **"Blueprint"**
3. Connect your GitHub account if not already connected
4. Select your repository
5. Render will automatically detect `render.yaml` and configure everything
6. Click **"Apply"** to start deployment

#### Option B: Manual Web Service

1. Go to https://dashboard.render.com/
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `meeting-assistant` (or any name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Choose **Free** plan or paid plan
6. Click **"Create Web Service"**

### 5. Wait for Deployment

- First deployment takes 2-5 minutes
- You can watch the build logs in real-time
- Once complete, Render provides your app URL: `https://your-app-name.onrender.com`

### 6. Post-Deployment Configuration

The app should work automatically since we're using `window.location.origin` for API calls. However, verify:

1. Visit your Render app URL
2. Test creating a meeting
3. Test recording/uploading audio

### 7. Optional: Environment Variables (for security)

For production, consider moving sensitive data to environment variables:

1. In Render Dashboard, go to your service
2. Navigate to **"Environment"** tab
3. Add variables:
   - `SUPABASE_URL`: Your Supabase URL
   - `SUPABASE_API_KEY`: Your Supabase API key

Then update `main.py` to read from environment variables:

```python
import os

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://alyjyarqzaoldlbczawz.supabase.co")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY", "your-default-key")
```

### 8. Custom Domain (Optional)

1. In Render Dashboard, go to your service
2. Navigate to **"Settings"** tab
3. Scroll to **"Custom Domain"**
4. Follow instructions to add your domain

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version compatibility

### App Doesn't Start

- Check that start command is correct: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Verify the service logs for errors

### CORS Issues

If you encounter CORS errors:

1. Update `main.py` CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-app-name.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Free Tier Limitations

- Free tier services spin down after 15 minutes of inactivity
- First request after inactivity may take 30-50 seconds (cold start)
- Consider upgrading to paid tier for always-on service

## Updating Your Deployment

After making changes to your code:

```bash
git add .
git commit -m "Your commit message"
git push
```

Render will automatically detect the push and redeploy your service.

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com/
