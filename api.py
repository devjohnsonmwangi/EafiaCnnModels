from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import importlib
import base64
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import io
from PIL import Image

print("api.py loaded")

app = FastAPI(
    title="TB CNN Detection API",
    description="Medical image analysis API for disease detection",
    version="1.0.0"
)

# CORS configuration - update with your frontend URL in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://cnn-disease-detection-system-server.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ImageInput(BaseModel):
    image_base64: str


class HealthResponse(BaseModel):
    status: str
    message: str


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    heatmap: Optional[str] = None
    model: str


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check API health and readiness"""
    return {
        "status": "operational",
        "message": "API is running"
    }


# Utility functions
def run_model(model_name: str, base64_image: str):
    """Run the specified model with base64 encoded image"""
    try:
        module = importlib.import_module(f"trained_models.{model_name}_model")

        if not hasattr(module, "handler"):
            return {
                "status": "error",
                "message": "handler() not found in model file"
            }

        result = module.handler(base64_image)
        return result

    except ModuleNotFoundError:
        return {
            "status": "error",
            "message": f"Model file '{model_name}_model.py' not found."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string"""
    return base64.b64encode(image_bytes).decode('utf-8')


def base64_to_image(base64_str: str) -> Image.Image:
    """Convert base64 string back to PIL Image"""
    if base64_str.startswith("data:image"):
        base64_str = base64_str.split(",")[1]
    
    image_bytes = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(image_bytes))


# Tuberculosis endpoints
@app.post("/predict/tuberculosis", response_model=PredictionResponse)
def predict_tb(data: ImageInput):
    """
    Predict tuberculosis from chest X-ray image.
    
    Expected input:
    - image_base64: Base64 encoded PNG/JPG image
    
    Returns:
    - prediction: "Normal" or "Tuberculosis"
    - confidence: Confidence score 0-1
    - heatmap: Base64 encoded heatmap (optional)
    """
    print("TB prediction requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("tuberculosis", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@app.post("/predict/tuberculosis/file")
async def predict_tb_file(file: UploadFile = File(...)):
    """
    Alternative endpoint: Upload image file directly
    
    Accepts: PNG, JPG, JPEG image files
    
    Returns:
    - prediction: "Normal" or "Tuberculosis"
    - confidence: Confidence score 0-1
    - heatmap: Base64 encoded heatmap (optional)
    """
    print("TB file prediction requested")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        base64_image = image_to_base64(contents)
        
        result = run_model("tuberculosis", base64_image)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Pneumonia endpoints
@app.post("/predict/pneumonia", response_model=PredictionResponse)
def predict_pneumonia(data: ImageInput):
    """Predict pneumonia from chest X-ray image"""
    print("Pneumonia prediction requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("pneumonia", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@app.post("/predict/pneumonia/file")
async def predict_pneumonia_file(file: UploadFile = File(...)):
    """Upload pneumonia X-ray file directly"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        base64_image = image_to_base64(contents)
        result = run_model("pneumonia", base64_image)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Bone Fracture endpoints
@app.post("/predict/bone_fracture", response_model=PredictionResponse)
def predict_fracture(data: ImageInput):
    """Predict bone fracture from X-ray image"""
    print("Bone fracture prediction requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("bone_fracture", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@app.post("/predict/bone_fracture/file")
async def predict_fracture_file(file: UploadFile = File(...)):
    """Upload bone X-ray file directly"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        base64_image = image_to_base64(contents)
        result = run_model("bone_fracture", base64_image)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Lung Cancer endpoints
@app.post("/predict/lung_cancer", response_model=PredictionResponse)
def predict_lung_cancer(data: ImageInput):
    """Predict lung cancer from chest X-ray image"""
    print("Lung cancer prediction requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("lung_cancer", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@app.post("/predict/lung_cancer/file")
async def predict_lung_cancer_file(file: UploadFile = File(...)):
    """Upload lung X-ray file directly"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        base64_image = image_to_base64(contents)
        result = run_model("lung_cancer", base64_image)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# X-Ray Detection endpoints
@app.post("/predict/xray_detection", response_model=PredictionResponse)
def detect_xray(data: ImageInput):
    """
    Detect whether an image is an X-ray or not.
    
    This is a prerequisite validation step to ensure uploaded images
    are actually medical X-rays before processing with disease-specific models.
    
    Expected input:
    - image_base64: Base64 encoded PNG/JPG image
    
    Returns:
    - prediction: "X-Ray" or "Not X-Ray"
    - confidence: Confidence score 0-1
    - is_xray: Boolean indicating if image is classified as X-ray
    """
    print("X-ray detection requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("xray_detector", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


@app.post("/predict/xray_detection/file")
async def detect_xray_file(file: UploadFile = File(...)):
    """
    Alternative endpoint: Upload image file directly for X-ray detection
    
    Accepts: PNG, JPG, JPEG image files
    
    Returns:
    - prediction: "X-Ray" or "Not X-Ray"
    - confidence: Confidence score 0-1
    - is_xray: Boolean indicating if image is classified as X-ray
    """
    print("X-ray file detection requested")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        base64_image = image_to_base64(contents)
        
        result = run_model("xray_detector", base64_image)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# X-Ray Validation endpoint (specifically for NestJS validation workflow)
@app.post("/predict/xray_validation", response_model=PredictionResponse)
def validate_xray(data: ImageInput):
    """
    Validate if an image is a valid medical X-ray.
    
    This endpoint is specifically designed for validating X-ray images
    before they are processed through disease-specific models.
    Used as a prerequisite validation step in the TB detection pipeline.
    
    Expected input:
    - image_base64: Base64 encoded PNG/JPG image
    
    Returns:
    - prediction: "X-Ray" or "Not X-Ray"
    - confidence: Confidence score 0-1
    - is_xray: Boolean indicating if image is classified as X-ray
    - heatmap_base64: Optional heatmap visualization
    """
    print("X-ray validation requested")
    
    if not data.image_base64:
        raise HTTPException(status_code=400, detail="No image data provided")
    
    result = run_model("xray_detector", data.image_base64)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    
    return result


# Info endpoints
@app.get("/info/models")
def get_models_info():
    """Get information about available models"""
    return {
        "models": [
            {
                "name": "xray_detection",
                "description": "Validates if an image is a medical X-ray",
                "type": "prerequisite",
                "endpoint": "/predict/xray_detection"
            },
            {
                "name": "tuberculosis",
                "description": "Detects tuberculosis from chest X-rays",
                "accuracy": "93.5%",
                "endpoint": "/predict/tuberculosis"
            },
            {
                "name": "pneumonia",
                "description": "Detects pneumonia from chest X-rays",
                "endpoint": "/predict/pneumonia"
            },
            {
                "name": "bone_fracture",
                "description": "Detects bone fractures from X-rays",
                "endpoint": "/predict/bone_fracture"
            },
            {
                "name": "lung_cancer",
                "description": "Detects lung cancer from chest X-rays",
                "endpoint": "/predict/lung_cancer"
            }
        ]
    }


# Root endpoint
@app.get("/")
def root():
    """API information and documentation"""
    return {
        "name": "TB CNN Detection System API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "GET /health",
            "models_info": "GET /info/models",
            "validate_xray": "POST /predict/xray_validation",
            "detect_xray": "POST /predict/xray_detection",
            "detect_xray_file": "POST /predict/xray_detection/file",
            "predict_tb": "POST /predict/tuberculosis",
            "predict_tb_file": "POST /predict/tuberculosis/file",
            "predict_pneumonia": "POST /predict/pneumonia",
            "predict_pneumonia_file": "POST /predict/pneumonia/file",
            "predict_lung_cancer": "POST /predict/lung_cancer",
            "predict_lung_cancer_file": "POST /predict/lung_cancer/file",
            "predict_bone_fracture": "POST /predict/bone_fracture",
            "predict_bone_fracture_file": "POST /predict/bone_fracture/file"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Handle 404
@app.get("/{path_name:path}")
def handle_404(path_name: str):
    """Handle undefined routes"""
    raise HTTPException(
        status_code=404,
        detail=f"Endpoint '/{path_name}' not found. Visit /docs for available endpoints."
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
