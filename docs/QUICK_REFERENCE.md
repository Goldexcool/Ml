# 🎯 Quick Command Reference

## Essential Commands (Copy & Paste)

### Starting the Server

```powershell
# Navigate to project
cd c:\Users\golde\OneDrive\Desktop\model

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start server
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

**Server will be at:** http://localhost:8000  
**Interactive docs:** http://localhost:8000/docs

---

### Testing the API

```powershell
# Test with random image
.\.venv\Scripts\python.exe test_image_upload.py

# Test health endpoint
Invoke-RestMethod http://localhost:8000/health
```

---

### GitHub Setup

```powershell
# Initialize Git
git init
git add .
git commit -m "Initial commit: FastAPI TensorFlow API"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

---

### Future Updates

```powershell
# After making changes
git add .
git commit -m "Description of changes"
git push
```

---

## File Locations

```
C:\Users\golde\OneDrive\Desktop\model\
│
├── 🐍 main.py                    # FastAPI application
├── 📦 requirements.txt           # Dependencies
├── 🚀 render.yaml               # Render deployment config
├── 🧪 test_api.py               # Test script (JSON)
├── 🧪 test_image_upload.py      # Test script (Image upload)
├── 🤖 tomato_leaf_cnn_model.h5   # Your trained model
│
├── 📖 README.md                  # Project overview
├── 📖 DEPLOYMENT_GUIDE.md        # GitHub + Render setup
├── 📖 REACT_INTEGRATION.md       # React frontend guide
├── 📖 SUMMARY.md                 # Complete summary
└── 📖 QUICK_REFERENCE.md         # This file
```

---

## API Endpoints Summary

| Endpoint | Method | Purpose | Example |
|----------|--------|---------|---------|
| `/` | GET | Root/health check | `curl http://localhost:8000/` |
| `/health` | GET | Detailed health | `curl http://localhost:8000/health` |
| `/api/analyze` | POST | Analyze image | See test script |
| `/docs` | GET | Interactive API docs | Open in browser |

---

## Test Image Upload (PowerShell)

```powershell
# Create form data with image
$image = "C:\path\to\tomato_leaf.jpg"
$form = @{ file = Get-Item $image }

# Upload
Invoke-RestMethod -Uri "http://localhost:8000/api/analyze" `
  -Method Post `
  -Form $form
```

---

## Test Image Upload (Python)

```python
import requests

# Upload image
with open('tomato_leaf.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files=files
    )
    result = response.json()
    print(f"Result: {result['label']}")
    print(f"Confidence: {result['confidence']}%")
```

---

## Common Issues & Fixes

### Issue: Port 8000 already in use
**Fix:** Use a different port
```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --port 8001
```

### Issue: Module not found
**Fix:** Reinstall dependencies
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Model file not found
**Fix:** Ensure `tomato_leaf_cnn_model.h5` is in project root

---

## Deployment URLs

**After deploying to Render:**

```
Production API:  https://YOUR-SERVICE-NAME.onrender.com
Health Check:    https://YOUR-SERVICE-NAME.onrender.com/health
API Docs:        https://YOUR-SERVICE-NAME.onrender.com/docs
```

---

## React Integration (Quick)

```javascript
// Upload image from React
const uploadImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    body: formData,
  });
  
  return await response.json();
};

// Usage
const result = await uploadImage(myImageFile);
console.log(result.label);        // "Diseased" or "Healthy"
console.log(result.confidence);   // 87.52
```

---

## Stop the Server

Press `Ctrl + C` in the terminal running uvicorn

---

## Environment Variables (Production)

Create `.env` file (if needed):

```env
PORT=8000
MODEL_PATH=tomato_leaf_cnn_model.h5
```

---

## Performance Tips

✅ Keep server running (no cold starts)  
✅ Use `--reload` only in development  
✅ Consider upgrading Render plan for production  
✅ Add caching for frequent predictions  
✅ Use CDN for frontend assets  

---

## Next Steps

1. ✅ **Test locally** - Run test scripts
2. 📤 **Push to GitHub** - Version control
3. 🚀 **Deploy to Render** - Go live
4. ⚛️ **Build React frontend** - User interface
5. 📊 **Monitor usage** - Analytics

---

## Useful Links

- **Project Folder**: `C:\Users\golde\OneDrive\Desktop\model`
- **Local API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **GitHub**: https://github.com (create repo)
- **Render**: https://render.com (deploy)

---

## Got Questions?

📖 Check the detailed guides:
- `README.md` - Project overview
- `DEPLOYMENT_GUIDE.md` - Deployment steps
- `REACT_INTEGRATION.md` - Frontend connection
- `SUMMARY.md` - Complete summary

---

**Last Updated:** November 4, 2025  
**Status:** ✅ Ready for deployment!
