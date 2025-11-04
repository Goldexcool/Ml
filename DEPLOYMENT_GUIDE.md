# Complete Deployment Guide

## 📦 Step-by-Step Deployment Tutorial

### ✅ What We've Done So Far

1. **Created Project Structure** ✅
   - `main.py` - FastAPI application
   - `requirements.txt` - Dependencies
   - `render.yaml` - Deployment configuration
   - `.gitignore` - Git ignore rules
   - `README.md` - Project documentation
   - `test_api.py` - API testing script

2. **Set Up Virtual Environment** ✅
   - Created Python 3.12 virtual environment
   - Installed all dependencies (FastAPI, TensorFlow, etc.)

3. **Tested Locally** ✅
   - API is running on http://localhost:8000
   - Model loads successfully
   - Endpoints are working

---

## 🚀 Next Steps: GitHub & Render Deployment

### Step 1: Initialize Git Repository

Open a **new** PowerShell terminal (keep the API running in the current one) and run:

```powershell
cd c:\Users\golde\OneDrive\Desktop\model

# Initialize Git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FastAPI TensorFlow Tomato Disease Classifier"
```

### Step 2: Create GitHub Repository

1. **Go to GitHub:**
   - Visit https://github.com/new
   - Or click the `+` icon → "New repository"

2. **Repository Settings:**
   - Repository name: `tomato-disease-classifier-api` (or your choice)
   - Description: `FastAPI + TensorFlow API for tomato disease classification`
   - Visibility: **Public** (required for Render free tier)
   - ⚠️ **Do NOT** initialize with README, .gitignore, or license (we already have these)

3. **Click "Create repository"**

### Step 3: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```powershell
# Add the remote repository (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/johndoe/tomato-disease-api.git
git branch -M main
git push -u origin main
```

You'll be prompted to sign in to GitHub if you haven't already.

### Step 4: Deploy on Render

#### 4.1 Create Render Account
1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up using your GitHub account (recommended) or email

#### 4.2 Connect GitHub Repository
1. Once logged in, click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"** and authorize Render
3. Find and select your repository: `tomato-disease-classifier-api`

#### 4.3 Configure Web Service
Render will auto-detect `render.yaml`. Verify these settings:

- **Name:** `tomato-disease-api` (or your choice)
- **Environment:** `Python 3`
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Instance Type:** `Free`

#### 4.4 Environment Variables (Optional)
Click **"Advanced"** to add environment variables if needed:
- `PYTHON_VERSION`: `3.12.0`
- `TF_CPP_MIN_LOG_LEVEL`: `2` (reduces TensorFlow warnings)

#### 4.5 Deploy
1. Click **"Create Web Service"**
2. Render will start building your app (this takes 5-10 minutes)
3. Watch the logs for any errors

### Step 5: Monitor Deployment

The deployment log will show:
```
==> Installing dependencies
==> Installing Python dependencies
==> Building application
==> Starting service
```

Once you see:
```
INFO:     Uvicorn running on http://0.0.0.0:10000
✅ Model loaded successfully
```

Your API is live! 🎉

---

## 🔍 Testing Your Deployed API

### Your API URL
```
https://YOUR-SERVICE-NAME.onrender.com
```

Example: `https://tomato-disease-api.onrender.com`

### Test Endpoints

**1. Root Endpoint (Browser or curl):**
```powershell
curl https://YOUR-SERVICE-NAME.onrender.com/
```

**2. Health Check:**
```powershell
curl https://YOUR-SERVICE-NAME.onrender.com/health
```

**3. Prediction (PowerShell):**
```powershell
$body = @{
    features = @(0.1, 0.2, 0.3, 0.4, 0.5) * 9830  # Adjust size for your model
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://YOUR-SERVICE-NAME.onrender.com/predict" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

---

## ⚠️ Important Notes

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 512 MB RAM limit
- 750 hours/month free

### Model File Size
- If your `tomato_leaf_cnn_model.h5` is >100MB, consider:
  1. Using Git LFS (Large File Storage)
  2. Hosting model on Google Drive/Dropbox and downloading in code
  3. Upgrading to Render paid tier

### Adding Git LFS (if model >100MB):
```powershell
# Install Git LFS
git lfs install

# Track .h5 files
git lfs track "*.h5"

# Add .gitattributes
git add .gitattributes

# Commit and push
git add tomato_leaf_cnn_model.h5
git commit -m "Add model file with Git LFS"
git push
```

---

## 🔄 Updating Your API

After making changes:

```powershell
# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push

# Render automatically redeploys! 🚀
```

---

## 🐛 Troubleshooting

### Build Fails
- Check `requirements.txt` versions
- Ensure `tomato_leaf_cnn_model.h5` is in repository
- Check Render logs for specific errors

### Model Doesn't Load
- Verify model file is in root directory
- Check model file size (<100MB for free tier)
- Ensure TensorFlow version compatibility

### Cold Start Issues
- First request after sleep is slow (normal)
- Consider upgrading to paid tier for always-on
- Or use a cron job to ping your API every 10 minutes

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **TensorFlow Docs:** https://www.tensorflow.org/

---

## ✅ Verification Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Repository connected to Render
- [ ] Service deployed successfully
- [ ] API responds to health checks
- [ ] Prediction endpoint works
- [ ] CORS configured for frontend

Once all checked, proceed to connecting your React frontend! →
