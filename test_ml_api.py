import requests
import base64
import json
from PIL import Image
import io

# API Base URL
API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False


def create_test_image():
    """Create a simple test image (numpy array converted to PIL Image)"""
    print("\n" + "="*60)
    print("Creating Test Image")
    print("="*60)
    try:
        import numpy as np
        # Create a simple grayscale image (simulating X-ray)
        img_array = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
        img = Image.fromarray(img_array, mode='L')
        
        # Convert to base64
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        
        print(f"✓ Test image created (256x256 grayscale)")
        print(f"✓ Base64 length: {len(base64_image)} characters")
        return base64_image
    except Exception as e:
        print(f"Error creating test image: {e}")
        return None


def test_tb_prediction(base64_image):
    """Test TB prediction endpoint"""
    print("\n" + "="*60)
    print("Testing TB Prediction Endpoint")
    print("="*60)
    print("Sending base64 encoded image to /predict/tuberculosis...")
    
    try:
        payload = {
            "image_base64": base64_image
        }
        response = requests.post(
            f"{API_URL}/predict/tuberculosis",
            json=payload,
            timeout=30
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ Prediction successful!")
            print(f"  - Prediction: {result.get('prediction')}")
            print(f"  - Confidence: {result.get('confidence')}")
            print(f"  - Model: {result.get('model')}")
            return True
        else:
            print(f"\n✗ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Connection Error: Could not connect to API")
        print(f"  Make sure the API is running at {API_URL}")
        return False
    except requests.exceptions.Timeout:
        print("✗ Timeout Error: Request took too long")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_models_info():
    """Get information about available models"""
    print("\n" + "="*60)
    print("Available Models")
    print("="*60)
    try:
        response = requests.get(f"{API_URL}/info/models")
        if response.status_code == 200:
            models = response.json()
            print(json.dumps(models, indent=2))
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    print("\n" + "#"*60)
    print("# TB CNN Detection API - Test Suite")
    print("#"*60)
    
    # Test health endpoint
    health_ok = test_health()
    
    if not health_ok:
        print("\n✗ API is not responding. Make sure it's running:")
        print("  cd cnn_models")
        print("  python api.py")
        return
    
    # Get available models
    test_models_info()
    
    # Create test image
    base64_image = create_test_image()
    
    if base64_image:
        # Test TB prediction
        test_tb_prediction(base64_image)
    
    print("\n" + "#"*60)
    print("# Test Suite Complete")
    print("#"*60)
    print("\nFor more testing, use Swagger UI: http://localhost:5000/docs")


if __name__ == "__main__":
    main()
