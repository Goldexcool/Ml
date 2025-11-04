"""
Test script for the FastAPI TensorFlow Model API
"""
import requests
import numpy as np
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    print("\n" + "="*50)
    print("Testing GET / (Root Endpoint)")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_health():
    """Test the health endpoint"""
    print("\n" + "="*50)
    print("Testing GET /health")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_model_info():
    """Test the model info endpoint"""
    print("\n" + "="*50)
    print("Testing GET /model-info")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_prediction():
    """Test the prediction endpoint with sample data"""
    print("\n" + "="*50)
    print("Testing POST /predict")
    print("="*50)
    
    # Create sample features (for a 128x128x3 image, that's 49152 features)
    # Flattened image data
    num_features = 128 * 128 * 3  # 49152
    sample_features = np.random.rand(num_features).tolist()
    
    payload = {
        "features": sample_features
    }
    
    print(f"Sending {len(sample_features)} features...")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response:")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Predicted Class: {result['predicted_class']}")
        print(f"  Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200


def run_all_tests():
    """Run all API tests"""
    print("\n" + "🚀 "*25)
    print("FastAPI TensorFlow Model API - Test Suite")
    print("🚀 "*25)
    
    tests = [
        ("Root Endpoint", test_root),
        ("Health Check", test_health),
        ("Model Info", test_model_info),
        ("Prediction", test_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")


if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API.")
        print("Make sure the server is running:")
        print("  .\\venv\\Scripts\\python.exe -m uvicorn main:app --reload")
