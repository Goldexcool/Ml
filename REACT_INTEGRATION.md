# React Frontend Integration Guide

## 🌐 Connecting Your React App to the FastAPI Backend

This guide shows you how to integrate your deployed FastAPI backend with a React frontend.

---

## 🎯 Overview

Your API provides these endpoints:
- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /predict` - Make predictions
- `GET /model-info` - Get model information

---

## 🔧 Setup: Installing Dependencies

In your React project:

```bash
npm install axios
# or
yarn add axios
```

---

## 📁 Project Structure (React)

```
my-react-app/
├── src/
│   ├── api/
│   │   └── modelApi.js          # API service
│   ├── components/
│   │   ├── ImageUploader.jsx    # Image upload component
│   │   └── PredictionResult.jsx # Display results
│   ├── App.jsx
│   └── main.jsx
├── .env                         # Environment variables
└── package.json
```

---

## ⚙️ Step 1: Configure API URL

Create `.env` file in your React project root:

```env
# For local development
VITE_API_URL=http://localhost:8000

# For production (uncomment and update after deployment)
# VITE_API_URL=https://your-service-name.onrender.com
```

**Note:** If using Create React App, use `REACT_APP_API_URL` instead.

---

## 📡 Step 2: Create API Service

Create `src/api/modelApi.js`:

```javascript
import axios from 'axios';

// Get API URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

/**
 * Check if API is running
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

/**
 * Get model information
 */
export const getModelInfo = async () => {
  try {
    const response = await apiClient.get('/model-info');
    return response.data;
  } catch (error) {
    console.error('Failed to get model info:', error);
    throw error;
  }
};

/**
 * Convert image to features array
 * @param {File} imageFile - The image file to process
 * @returns {Promise<number[]>} - Flattened array of pixel values
 */
export const imageToFeatures = async (imageFile) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    
    reader.onload = (e) => {
      const img = new Image();
      
      img.onload = () => {
        // Create canvas to process image
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Resize to model input size (adjust based on your model)
        canvas.width = 128;
        canvas.height = 128;
        
        // Draw and resize image
        ctx.drawImage(img, 0, 0, 128, 128);
        
        // Get image data
        const imageData = ctx.getImageData(0, 0, 128, 128);
        const pixels = imageData.data;
        
        // Convert to normalized array (0-1 range)
        const features = [];
        for (let i = 0; i < pixels.length; i += 4) {
          // RGB values (skip alpha channel)
          features.push(pixels[i] / 255.0);     // R
          features.push(pixels[i + 1] / 255.0); // G
          features.push(pixels[i + 2] / 255.0); // B
        }
        
        resolve(features);
      };
      
      img.onerror = reject;
      img.src = e.target.result;
    };
    
    reader.onerror = reject;
    reader.readAsDataURL(imageFile);
  });
};

/**
 * Make prediction
 * @param {number[]} features - Array of numerical features
 * @returns {Promise<Object>} - Prediction result
 */
export const makePrediction = async (features) => {
  try {
    const response = await apiClient.post('/predict', {
      features: features,
    });
    return response.data;
  } catch (error) {
    console.error('Prediction failed:', error);
    throw error;
  }
};

/**
 * Predict from image file
 * @param {File} imageFile - Image file to classify
 * @returns {Promise<Object>} - Prediction result
 */
export const predictFromImage = async (imageFile) => {
  try {
    // Convert image to features
    const features = await imageToFeatures(imageFile);
    
    // Make prediction
    const result = await makePrediction(features);
    
    return result;
  } catch (error) {
    console.error('Prediction from image failed:', error);
    throw error;
  }
};

export default {
  checkHealth,
  getModelInfo,
  makePrediction,
  predictFromImage,
};
```

---

## 🖼️ Step 3: Create Image Uploader Component

Create `src/components/ImageUploader.jsx`:

```jsx
import React, { useState } from 'react';
import { predictFromImage } from '../api/modelApi';

const ImageUploader = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleImageSelect = (event) => {
    const file = event.target.files[0];
    
    if (file) {
      setSelectedImage(file);
      setError(null);
      setPrediction(null);
      
      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handlePredict = async () => {
    if (!selectedImage) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await predictFromImage(selectedImage);
      setPrediction(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Prediction failed. Please try again.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getClassName = (predictedClass) => {
    // Adjust based on your model's classes
    const classes = ['Healthy', 'Diseased'];
    return classes[predictedClass] || `Class ${predictedClass}`;
  };

  return (
    <div className="image-uploader">
      <h2>Tomato Disease Classifier</h2>
      
      {/* File Input */}
      <div className="upload-section">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageSelect}
          id="image-input"
          style={{ display: 'none' }}
        />
        <label htmlFor="image-input" className="upload-button">
          Choose Image
        </label>
      </div>

      {/* Image Preview */}
      {imagePreview && (
        <div className="image-preview">
          <img src={imagePreview} alt="Selected" style={{ maxWidth: '400px' }} />
        </div>
      )}

      {/* Predict Button */}
      {selectedImage && (
        <button 
          onClick={handlePredict} 
          disabled={loading}
          className="predict-button"
        >
          {loading ? 'Analyzing...' : 'Analyze Image'}
        </button>
      )}

      {/* Loading Indicator */}
      {loading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Processing image...</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <p>❌ {error}</p>
        </div>
      )}

      {/* Prediction Result */}
      {prediction && (
        <div className="prediction-result">
          <h3>Results</h3>
          <div className="result-card">
            <p className="result-class">
              <strong>Prediction:</strong> {getClassName(prediction.predicted_class)}
            </p>
            <p className="result-confidence">
              <strong>Confidence:</strong> {(prediction.confidence * 100).toFixed(2)}%
            </p>
            <div className="confidence-bar">
              <div 
                className="confidence-fill"
                style={{ width: `${prediction.confidence * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
```

---

## 🎨 Step 4: Add Styling

Create `src/components/ImageUploader.css`:

```css
.image-uploader {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.image-uploader h2 {
  text-align: center;
  color: #333;
  margin-bottom: 2rem;
}

.upload-section {
  text-align: center;
  margin-bottom: 2rem;
}

.upload-button {
  display: inline-block;
  padding: 12px 24px;
  background-color: #4CAF50;
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.upload-button:hover {
  background-color: #45a049;
}

.image-preview {
  text-align: center;
  margin: 2rem 0;
}

.image-preview img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.predict-button {
  display: block;
  width: 100%;
  padding: 14px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: 1rem 0;
}

.predict-button:hover:not(:disabled) {
  background-color: #0b7dda;
}

.predict-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 2rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #2196F3;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  text-align: center;
}

.prediction-result {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.prediction-result h3 {
  margin-top: 0;
  color: #333;
}

.result-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-class, .result-confidence {
  font-size: 18px;
  margin: 0.5rem 0;
}

.confidence-bar {
  width: 100%;
  height: 24px;
  background-color: #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  margin-top: 1rem;
}

.confidence-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  transition: width 0.3s ease;
}
```

---

## 🔗 Step 5: Use in App

Update `src/App.jsx`:

```jsx
import React, { useEffect, useState } from 'react';
import ImageUploader from './components/ImageUploader';
import { checkHealth } from './api/modelApi';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    // Check API health on mount
    const checkApiHealth = async () => {
      try {
        await checkHealth();
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
      }
    };

    checkApiHealth();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🍅 Tomato Disease Classifier</h1>
        <div className={`api-status ${apiStatus}`}>
          API Status: {apiStatus === 'online' ? '🟢 Online' : apiStatus === 'offline' ? '🔴 Offline' : '🟡 Checking...'}
        </div>
      </header>

      <main>
        {apiStatus === 'online' ? (
          <ImageUploader />
        ) : (
          <div className="api-offline-message">
            <p>⚠️ API is currently offline. Please try again later.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
```

---

## 🚀 Step 6: Running Your App

### Development Mode

```bash
# Make sure API is running on http://localhost:8000
npm run dev
# or
yarn dev
```

### Production Build

```bash
# Update .env with production API URL
VITE_API_URL=https://your-service-name.onrender.com

# Build
npm run build
# or
yarn build
```

---

## 🌐 Step 7: Deploy React App

### Option 1: Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Option 2: Netlify

```bash
npm install -g netlify-cli
netlify deploy --prod
```

### Option 3: Render Static Site

1. Go to Render Dashboard
2. Click "New +" → "Static Site"
3. Connect your React repository
4. Build command: `npm run build`
5. Publish directory: `dist` (Vite) or `build` (CRA)

---

## 🔒 CORS Verification

Your API already has CORS enabled for all origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

For production, you should restrict origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "https://your-frontend.netlify.app",
        "http://localhost:5173",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### CORS Errors
- Ensure API has CORS middleware configured
- Check browser console for specific CORS errors
- Verify API URL in `.env` file

### Network Errors
- Check if API is running
- Verify API URL is correct
- Check network tab in browser DevTools

### Slow First Request
- Render free tier has cold starts (~30s)
- Show loading indicator
- Consider upgrading to paid tier

---

## 📱 Example: Complete Integration

Here's a complete minimal example:

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'https://your-service-name.onrender.com';

function SimplePrediction() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/predict`, {
        features: Array(49152).fill(0).map(() => Math.random()),
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Predicting...' : 'Make Prediction'}
      </button>
      {result && (
        <div>
          <p>Class: {result.predicted_class}</p>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}

export default SimplePrediction;
```

---

## ✅ Checklist

- [ ] API deployed and accessible
- [ ] `.env` file created with API URL
- [ ] axios installed
- [ ] API service created
- [ ] Components created
- [ ] CORS configured
- [ ] Tested locally
- [ ] Deployed frontend
- [ ] End-to-end testing complete

---

## 🎉 You're Done!

Your React app is now connected to your FastAPI + TensorFlow backend!

**Next Steps:**
- Add more features (batch prediction, history, etc.)
- Improve error handling
- Add loading states
- Implement authentication if needed
- Monitor performance with analytics

Happy coding! 🚀
