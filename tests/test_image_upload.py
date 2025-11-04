"""
Test script for image upload to Tomato Disease Classifier API
Creates a test image and uploads it to the API
"""
import requests
import numpy as np
from PIL import Image
import io

# API URL
API_URL = "http://localhost:8000"

def create_test_image(size=(128, 128)):
    """Create a random test image"""
    # Create random RGB image
    img_array = np.random.randint(0, 256, (size[0], size[1], 3), dtype=np.uint8)
    img = Image.fromarray(img_array, 'RGB')
    return img

def test_image_upload():
    """Test the /api/analyze endpoint with an image"""
    print("\n" + "="*60)
    print("🍅 Testing Tomato Disease Classifier API")
    print("="*60)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"\n✅ API Status: {response.json()['status']}")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: API is not running!")
        print("Start the server with:")
        print("  .\\venv\\Scripts\\python.exe -m uvicorn main:app --reload")
        return
    
    # Create test image
    print("\n📸 Creating test image...")
    test_img = create_test_image()
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    test_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Upload to API
    print("📤 Uploading image to /api/analyze...")
    files = {'file': ('test_image.png', img_byte_arr, 'image/png')}
    
    try:
        response = requests.post(f"{API_URL}/api/analyze", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ SUCCESS! Analysis Complete")
            print("-" * 60)
            print(f"🏷️  Label:       {result['label']}")
            print(f"📊 Confidence:  {result['confidence']:.2f}%")
            print(f"🔢 Raw Score:   {result['raw_prediction']:.4f}")
            print(f"🩺 Diseased:    {result['is_diseased']}")
            print(f"📝 Message:     {result['message']}")
            print("-" * 60)
            
            # Confidence bar
            bar_length = 40
            filled_length = int(bar_length * result['confidence'] / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            print(f"\nConfidence: [{bar}] {result['confidence']:.1f}%")
            
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(response.json())
            
    except Exception as e:
        print(f"\n❌ Error uploading image: {e}")

def test_with_real_image(image_path):
    """Test with a real image file"""
    print(f"\n📸 Testing with real image: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_URL}/api/analyze", files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("\n✅ Analysis Complete")
                print(f"Label: {result['label']}")
                print(f"Confidence: {result['confidence']:.2f}%")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test with generated image
    test_image_upload()
    
    # Optional: Test with a real image
    # Uncomment and provide path to a tomato leaf image
    # test_with_real_image("C:\\path\\to\\your\\tomato_leaf_image.jpg")
    
    print("\n" + "="*60)
    print("🎉 Testing Complete!")
    print("="*60)
    print("\n💡 To test with your own image:")
    print("   1. Uncomment the test_with_real_image() line")
    print("   2. Provide the path to your tomato leaf image")
    print("\n📚 Visit http://localhost:8000/docs for interactive testing")
    print("="*60 + "\n")
