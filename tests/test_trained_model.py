"""
Test the newly trained 10-class model
"""
import requests
import os
from pathlib import Path

# Test with a real image from the dataset
test_image_dirs = [
    r"C:\Users\golde\Downloads\tomato\val\Tomato___healthy",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Early_blight",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Late_blight",
]

print("="*60)
print("🧪 TESTING NEWLY TRAINED MODEL")
print("="*60)

# Test health endpoint
print("\n1️⃣ Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

# Test with images from different classes
print("\n2️⃣ Testing image classification...")
for test_dir in test_image_dirs:
    if os.path.exists(test_dir):
        # Get first image from directory
        images = list(Path(test_dir).glob("*.jpg")) + list(Path(test_dir).glob("*.JPG"))
        if images:
            test_image = images[0]
            class_name = os.path.basename(test_dir).replace("Tomato___", "")
            
            print(f"\n📸 Testing: {class_name}")
            print(f"   Image: {test_image.name}")
            
            try:
                with open(test_image, 'rb') as f:
                    files = {'file': (test_image.name, f, 'image/jpeg')}
                    response = requests.post("http://localhost:8000/api/analyze", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Predicted: {result['disease']}")
                    print(f"   🎯 Confidence: {result['confidence']}%")
                    print(f"   🌿 Healthy: {result['is_healthy']}")
                    
                    # Show top 3 predictions
                    probs = result.get('all_probabilities', {})
                    if probs:
                        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
                        print(f"   📊 Top 3:")
                        for disease, prob in sorted_probs:
                            print(f"      - {disease}: {prob}%")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    print(f"   {response.text}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        break  # Test just one image for now

print("\n" + "="*60)
print("✅ Testing complete!")
print("="*60)
