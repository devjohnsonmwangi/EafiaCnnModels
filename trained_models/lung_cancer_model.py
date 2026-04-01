import os, base64
from io import BytesIO
from PIL import Image, ImageFile
import torch
import torch.nn as nn
from torchvision import models, transforms
from utils.heatmap import generate_heatmap

ImageFile.LOAD_TRUNCATED_IMAGES = True
device = torch.device("cpu")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAGE1_PATH = os.path.join(BASE_DIR, "..", "pth_files", "Normal_Abnormal_lungcancer_classifier.pth")
STAGE2_PATH = os.path.join(BASE_DIR, "..", "pth_files", "bm_classifier.pth")

def load_stage1():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(STAGE1_PATH, map_location=device))
    model.to(device)
    model.eval()
    return model

def load_stage2():
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(STAGE2_PATH, map_location=device))
    model.to(device)
    model.eval()
    return model

stage1 = load_stage1()
stage2 = load_stage2()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

class_stage1 = ["Normal", "Abnormal"]
class_stage2 = ["Benign", "Malignant"]

def handler(base64_image: str):
    try:
        if not base64_image:
            return {"status": "error", "message": "No image data provided"}

        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",")[1]

        image_bytes = base64.b64decode(base64_image)
        original_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        img_tensor = transform(original_image).unsqueeze(0).to(device)

        with torch.no_grad():
            out1 = stage1(img_tensor)
            pred1 = out1.argmax(1).item()
            label1 = class_stage1[pred1]

        pred2 = None
        final_label = label1
        if label1 == "Abnormal":
            out2 = stage2(img_tensor)
            pred2 = out2.argmax(1).item()
            final_label = class_stage2[pred2]

        chosen_model = stage2 if label1 == "Abnormal" else stage1
        target_idx = pred2 if label1 == "Abnormal" else pred1

        heatmap_base64 = generate_heatmap(chosen_model, img_tensor, original_image, target_idx)

        return {
            "status": "success",
            "stage1_prediction": label1,
            "final_prediction": final_label,
            "heatmap_base64": heatmap_base64
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
