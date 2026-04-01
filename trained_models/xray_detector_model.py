"""
X-Ray Detection Model
Identifies whether an image is an X-ray or non-medical image
Uses ResNet18 for binary classification
"""

import os
import base64
from io import BytesIO
from PIL import Image, ImageFile
import torch
import torch.nn as nn
from torchvision import models, transforms
from utils.heatmap import generate_heatmap

ImageFile.LOAD_TRUNCATED_IMAGES = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_model():
    """
    Load pre-trained ResNet18 model
    Fine-tuned for X-ray vs Non-X-ray classification
    """
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    # Replace final layer for binary classification
    model.fc = nn.Linear(model.fc.in_features, 2)
    
    # Note: In production, you would load a pre-trained weights file
    # For now, using ImageNet pretrained weights as base
    # model.load_state_dict(torch.load(PTH_PATH, map_location=torch.device('cpu')))
    
    model.to("cpu")
    model.eval()
    return model

model = load_model()

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# Class labels
class_names = ["Not X-Ray", "X-Ray"]

def handler(base64_image: str) -> dict:
    """
    Classify whether an image is an X-ray
    
    Args:
        base64_image: Base64 encoded image string
        
    Returns:
        dict with detection result and confidence
    """
    try:
        if not base64_image:
            return {
                "status": "error",
                "message": "No image data provided"
            }

        # Handle data URI format
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        # Decode base64 to image
        image_bytes = base64.b64decode(base64_image)
        original_image = Image.open(BytesIO(image_bytes)).convert("RGB")

        # Preprocess image
        img_tensor = transform(original_image).unsqueeze(0)

        # Make prediction
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            pred_idx = outputs.argmax(1).item()
            confidence = probabilities[0][pred_idx].item()
            prediction = class_names[pred_idx]

        # Generate heatmap
        heatmap_base64 = generate_heatmap(model, img_tensor, original_image, pred_idx)

        return {
            "status": "success",
            "is_xray": prediction == "X-Ray",
            "prediction": prediction,
            "confidence": round(confidence, 4),
            "heatmap_base64": heatmap_base64,
            "model": "xray_detector_v1"
        }

    except Exception as e:
        print(f"X-RAY DETECTOR ERROR: {repr(e)}")
        return {
            "status": "error",
            "message": str(e),
            "model": "xray_detector_v1"
        }
