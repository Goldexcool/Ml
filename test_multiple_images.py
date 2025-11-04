"""
Test multiple images from different disease classes
"""
import requests
import os
from pathlib import Path

# Test images from all classes
test_dirs = [
    r"C:\Users\golde\Downloads\tomato\val\Tomato___healthy",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Early_blight",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Late_blight",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Bacterial_spot",
    r"C:\Users\golde\Downloads\tomato\val\Tomato___Leaf_Mold",
]

print("="*70)
print("🧪 TESTING TRAINED MODEL - MULTIPLE DISEASE CLASSES")
print("="*70)

correct = 0
total = 0

for test_dir in test_dirs:
    if os.path.exists(test_dir):
        # Get first image
        images = list(Path(test_dir).glob("*.jpg")) + list(Path(test_dir).glob("*.JPG"))
        if images:
            test_image = images[0]
            expected_class = os.path.basename(test_dir).replace("Tomato___", "").replace("_", " ")
            
            print(f"\n📂 Expected: {expected_class}")
            print(f"   📸 Image: {test_image.name}")
            
            try:
                with open(test_image, 'rb') as f:
                    files = {'file': (test_image.name, f, 'image/jpeg')}
                    response = requests.post("http://localhost:8000/api/analyze", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    predicted = result['disease'].replace("_", " ")
                    
                    # Check if correct (case insensitive, handle spaces)
                    is_correct = expected_class.lower() == predicted.lower()
                    if is_correct:
                        print(f"   ✅ CORRECT: {result['disease']}")
                        correct += 1
                    else:
                        print(f"   ❌ WRONG: Predicted {result['disease']}")
                    
                    total += 1
                    print(f"   🎯 Confidence: {result['confidence']}%")
                    
                    # Show top 3
                    probs = result.get('all_probabilities', {})
                    if probs:
                        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
                        print(f"   📊 Top 3 predictions:")
                        for i, (disease, prob) in enumerate(sorted_probs, 1):
                            marker = "🎯" if i == 1 else "  "
                            print(f"      {marker} {i}. {disease}: {prob}%")
                else:
                    print(f"   ❌ Error: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

print("\n" + "="*70)
if total > 0:
    accuracy = (correct / total) * 100
    print(f"📊 ACCURACY: {correct}/{total} correct = {accuracy:.1f}%")
else:
    print("❌ No tests completed")
print("="*70)
