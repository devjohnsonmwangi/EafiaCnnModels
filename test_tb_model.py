#!/usr/bin/env python
"""
Test script to verify TB model API is ready for classifications
"""

import requests
import base64
from PIL import Image
import io
import json

# API Configuration
API_URL = "http://localhost:5000"
TB_ENDPOINT = f"{API_URL}/predict/tuberculosis"

def create_test_image(width=224, height=224):
    """Create a simple test image"""
    # Create a grayscale image (simulating X-ray)
    image = Image.new('L', (width, height), color=100)
    
    # Add some patterns to make it look more like an X-ray
    pixels = image.load()
    for i in range(0, width, 20):
        for j in range(0, height, 20):
            pixels[i, j] = 200
    
    return image

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def test_health_endpoint():
    """Test API health endpoint"""
    print("=" * 60)
    print("Testing TB Model API Health")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Health Check: {data.get('status')}")
        print(f"   Message: {data.get('message')}")
        return True
    except Exception as e:
        print(f"❌ Health Check Failed: {str(e)}")
        return False

def test_tb_classification():
    """Test TB classification endpoint"""
    print("\n" + "=" * 60)
    print("Testing TB Classification Model")
    print("=" * 60)
    
    try:
        # Create test image
        print("Creating test X-ray image...")
        test_image = create_test_image()
        base64_image = image_to_base64(test_image)
        
        print(f"Test image created: 224x224 PNG")
        print(f"Base64 string length: {len(base64_image)} characters")
        
        # Send classification request
        print("\nSending classification request to Flask API...")
        payload = {"image_base64": base64_image}
        
        response = requests.post(
            TB_ENDPOINT,
            json=payload,
            timeout=60,  # 60 second timeout for model inference
            headers={"Content-Type": "application/json"}
        )
        
        response.raise_for_status()
        result = response.json()
        
        # Display results
        print("\n" + "✅ Classification Successful!")
        print("-" * 60)
        print(f"Prediction: {result.get('prediction')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Model: {result.get('model')}")
        
        has_heatmap = "heatmap" in result and result.get("heatmap")
        print(f"Heatmap: {'✅ Available' if has_heatmap else '❌ Not available'}")
        
        if has_heatmap:
            heatmap_b64 = result.get("heatmap", "")
            print(f"Heatmap Base64 length: {len(heatmap_b64)} characters")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Request timed out - model may be processing slowly")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - API may not be running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Classification Failed: {str(e)}")
        if hasattr(e, 'response'):
            try:
                print(f"Error details: {e.response.json()}")
            except:
                pass
        return False

def test_file_endpoint():
    """Test file upload endpoint"""
    print("\n" + "=" * 60)
    print("Testing TB Classification File Endpoint")
    print("=" * 60)
    
    try:
        # Create test image
        print("Creating test image file...")
        test_image = create_test_image()
        
        # Save to temporary buffer
        buffer = io.BytesIO()
        test_image.save(buffer, format="PNG")
        buffer.seek(0)
        
        print("Sending file to Flask API...")
        
        files = {'file': ('test_xray.png', buffer, 'image/png')}
        response = requests.post(
            f"{API_URL}/predict/tuberculosis/file",
            files=files,
            timeout=60
        )
        
        response.raise_for_status()
        result = response.json()
        
        print("\n✅ File Classification Successful!")
        print("-" * 60)
        print(f"Prediction: {result.get('prediction')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Model: {result.get('model')}")
        
        return True
        
    except Exception as e:
        print(f"❌ File Classification Failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " TB MODEL API READINESS TEST ".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print(f"\nAPI URL: {API_URL}")
    print(f"Testing at: {__name__}\n")
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_endpoint()))
    results.append(("TB Classification (Base64)", test_tb_classification()))
    results.append(("TB Classification (File Upload)", test_file_endpoint()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 TB Model API is READY for classifications!")
    else:
        print("\n⚠️  Some tests failed. Check configuration and logs.")
    
    print("=" * 60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
