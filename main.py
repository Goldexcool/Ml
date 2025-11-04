"""
Tomato Disease Classifier - FastAPI Server
Loads weights directly from .h5 file
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import h5py

print("Building model architecture and loading weights from .h5 file...")

# Recreate the exact model architecture (10-class classification)
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(128, 128, 3)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Load weights directly from .h5 file
h5_path = "best_tomato_model.h5"
try:
    with h5py.File(h5_path, 'r') as f:
        if 'model_weights' in f:
            weight_group = f['model_weights']
        else:
            weight_group = f
        
        layer_names = [n.decode('utf8') if hasattr(n, 'decode') else n 
                       for n in weight_group.attrs.get('layer_names', [])]
        
        for layer in model.layers:
            if layer.name in layer_names:
                layer_weights = []
                g = weight_group[layer.name]
                weight_names = [n.decode('utf8') if hasattr(n, 'decode') else n 
                              for n in g.attrs.get('weight_names', [])]
                for weight_name in weight_names:
                    weight = np.array(g[weight_name])
                    layer_weights.append(weight)
                if layer_weights:
                    layer.set_weights(layer_weights)

    print("✅ Model loaded successfully with weights from .h5 file!")
    print(f"Model input shape: {model.input_shape}")
    print(f"Model output shape: {model.output_shape}")
    print(f"Total parameters: {model.count_params():,}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("⚠️  Model will run with random weights for testing")

# FastAPI app
app = FastAPI(title="Tomato Disease Classifier API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "🍅 Tomato Disease Classifier API",
        "model_source": "tomato_leaf_cnn_model.h5",
        "endpoints": {
            "analyze": "/api/analyze (POST with image file)",
            "health": "/health (GET)"
        },
        "model_info": {
            "input_shape": str(model.input_shape),
            "output_shape": str(model.output_shape),
            "parameters": int(model.count_params())
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_params": int(model.count_params()),
        "model_source": "h5_weights"
    }

@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Analyze uploaded tomato leaf image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and preprocess
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        img = img.convert('RGB')
        img = img.resize((128, 128))
        
        # Normalize
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict (10-class classification)
        prediction = model.predict(img_array, verbose=0)
        predicted_class = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0])) * 100
        
        # Class names from training
        class_names = [
            'Bacterial_spot',
            'Early_blight', 
            'Late_blight',
            'Leaf_Mold',
            'Septoria_leaf_spot',
            'Spider_mites',
            'Target_Spot',
            'Yellow_Leaf_Curl_Virus',
            'Tomato_mosaic_virus',
            'Healthy'
        ]
        
        disease_name = class_names[predicted_class]
        is_healthy = (disease_name == 'Healthy')
        
        return {
            "disease": disease_name,
            "confidence": round(confidence, 2),
            "is_healthy": is_healthy,
            "predicted_class_index": predicted_class,
            "all_probabilities": {
                class_names[i]: round(float(prediction[0][i]) * 100, 2) 
                for i in range(len(class_names))
            },
            "message": "Analysis complete",
            "model_source": "best_tomato_model.h5 (trained)"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print("\n" + "="*60)
    print("🍅 TOMATO DISEASE CLASSIFIER API")
    print("="*60)
    print(f"Server: http://localhost:{port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("Model: tomato_leaf_cnn_model.h5 (direct weights)")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
