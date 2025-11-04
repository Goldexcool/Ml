# TensorFlow Model API

A FastAPI-based REST API for serving TensorFlow model predictions with CORS support for React frontends.

## 📋 Features

- ✅ FastAPI framework for high performance
- ✅ TensorFlow model inference
- ✅ CORS enabled for frontend integration
- ✅ Health check endpoints
- ✅ Comprehensive error handling
- ✅ Ready for deployment on Render

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd model
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the API

```powershell
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### GET `/`
Health check endpoint
```json
{
  "message": "API is running",
  "status": "healthy",
  "model_loaded": true
}
```

### GET `/health`
Detailed health information
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_input_shape": "(None, 224, 224, 3)",
  "model_output_shape": "(None, 10)"
}
```

### POST `/predict`
Make predictions with the model

**Request:**
```json
{
  "features": [0.1, 0.2, 0.3, 0.4, 0.5]
}
```

**Response:**
```json
{
  "prediction": [0.1, 0.2, 0.3, 0.15, 0.25],
  "predicted_class": 4,
  "confidence": 0.25
}
```

### GET `/model-info`
Get model information
```json
{
  "model_path": "tomato_leaf_cnn_model.h5",
  "input_shape": "(None, 224, 224, 3)",
  "output_shape": "(None, 10)",
  "total_params": 1000000,
  "layers": 20
}
```

## 🧪 Testing

### Using curl (PowerShell)

**Test health endpoint:**
```powershell
curl http://localhost:8000/
```

**Test prediction endpoint:**
```powershell
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{"features": [0.1, 0.2, 0.3, 0.4, 0.5]}'
```

### Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8000/predict`
3. Set Headers: `Content-Type: application/json`
4. Set Body (raw JSON):
```json
{
  "features": [0.1, 0.2, 0.3, 0.4, 0.5]
}
```
5. Click Send

## 🌐 Deployment on Render

### Prerequisites
- GitHub account
- Render account (free tier available)

### Steps

1. **Push to GitHub:**
```powershell
git init
git add .
git commit -m "Initial commit: FastAPI TensorFlow API"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)

3. **Your API will be live at:**
   `https://your-service-name.onrender.com`

## 🔗 React Frontend Integration

### Example React Code

```javascript
// API service
const API_URL = 'https://your-service-name.onrender.com';

async function makePrediction(features) {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ features }),
    });
    
    if (!response.ok) {
      throw new Error('Prediction failed');
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

// Usage in component
function PredictionComponent() {
  const [result, setResult] = useState(null);
  
  const handlePredict = async () => {
    const features = [0.1, 0.2, 0.3, 0.4, 0.5];
    const prediction = await makePrediction(features);
    setResult(prediction);
  };
  
  return (
    <div>
      <button onClick={handlePredict}>Get Prediction</button>
      {result && (
        <div>
          <p>Predicted Class: {result.predicted_class}</p>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
```

## 📝 Environment Variables

For local development, create a `.env` file:
```
PORT=8000
```

## 🛠️ Tech Stack

- **FastAPI** - Modern Python web framework
- **TensorFlow** - Machine learning framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **NumPy** - Numerical computing

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.
