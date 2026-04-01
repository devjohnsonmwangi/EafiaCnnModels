# Backend API Documentation

## Overview

The TB CNN Detection System backend is a FastAPI-based REST API that provides medical image analysis endpoints for disease detection from X-ray and medical imaging data.

**Base URL**: `http://localhost:8000`  
**API Specification**: Open in browser at `/docs` for interactive Swagger UI

---

## Features

✅ **Multiple Disease Detection Models**
- Tuberculosis (TB) detection
- Pneumonia detection
- Bone fracture detection
- Lung cancer detection

✅ **Dual Input Methods**
- Base64 encoded images (JSON payload)
- Direct file upload (FormData)

✅ **Enhanced Response Data**
- Prediction label (Normal/Abnormal/Disease name)
- Confidence score (0-1)
- Grad-CAM heatmap visualization
- Model information

✅ **Production Ready**
- CORS enabled for frontend integration
- Error handling with descriptive messages
- Request validation
- Comprehensive documentation
- Health checks

---

## API Endpoints

### Health & Info

#### Health Check
```
GET /health
```

**Response**:
```json
{
  "status": "operational",
  "message": "API is running"
}
```

#### Root Information
```
GET /
```

**Response**:
```json
{
  "name": "TB CNN Detection System API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": { ... }
}
```

#### Models Information
```
GET /info/models
```

**Response**:
```json
{
  "models": [
    {
      "name": "tuberculosis",
      "description": "Detects tuberculosis from chest X-rays",
      "accuracy": "93.5%",
      "endpoint": "/predict/tuberculosis"
    },
    ...
  ]
}
```

---

### Tuberculosis Prediction

#### Method 1: base64 Encoded Image (Recommended)
```
POST /predict/tuberculosis
Content-Type: application/json

{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```

**Request Body**:
- `image_base64` (string, required): Base64 encoded image string

**Response**:
```json
{
  "prediction": "Normal",
  "confidence": 0.95,
  "heatmap": "iVBORw0KGgoAAAANSUhEUgAAAAUA...",
  "model": "tuberculosis"
}
```

**Status Codes**:
- `200 OK`: Prediction successful
- `400 Bad Request`: Invalid image format or no image provided
- `500 Internal Server Error`: Model processing error

#### Method 2: File Upload
```
POST /predict/tuberculosis/file
Content-Type: multipart/form-data

file: <binary image data>
```

**Parameters**:
- `file` (file, required): Image file (PNG, JPG, JPEG, GIF, WebP)

**Response**: Same as Method 1

---

### Pneumonia Prediction

#### Base64 Method
```
POST /predict/pneumonia
Content-Type: application/json

{
  "image_base64": "..."
}
```

#### File Upload
```
POST /predict/pneumonia/file
Content-Type: multipart/form-data

file: <binary image data>
```

---

### Bone Fracture Prediction

#### Base64 Method
```
POST /predict/bone_fracture
Content-Type: application/json

{
  "image_base64": "..."
}
```

#### File Upload
```
POST /predict/bone_fracture/file
Content-Type: multipart/form-data

file: <binary image data>
```

---

### Lung Cancer Prediction

#### Base64 Method
```
POST /predict/lung_cancer
Content-Type: application/json

{
  "image_base64": "..."
}
```

#### File Upload
```
POST /predict/lung_cancer/file
Content-Type: multipart/form-data

file: <binary image data>
```

---

## Response Format

### Success Response
```json
{
  "prediction": "Normal|Tuberculosis|Pneumonia|Fracture|Cancer",
  "confidence": 0.927,
  "heatmap": "base64_encoded_visualization",
  "model": "model_name"
}
```

**Fields**:
- `prediction` (string): The predicted class
- `confidence` (float): Confidence score from 0 to 1
- `heatmap` (string, optional): Base64 encoded Grad-CAM visualization
- `model` (string): Model name used for prediction

### Error Response
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Usage Examples

### cURL

**Tuberculosis Prediction with Base64**:
```bash
curl -X POST "http://localhost:8000/predict/tuberculosis" \
  -H "Content-Type: application/json" \
  -d '{"image_base64":"iVBORw0KGgoAAAANSUhEUgAAAAUA..."}'
```

**Tuberculosis Prediction with File**:
```bash
curl -X POST "http://localhost:8000/predict/tuberculosis/file" \
  -F "file=@chest_xray.png"
```

### JavaScript/TypeScript

See `src/services/tbApi.ts` for complete implementation.

```typescript
import { tbApi } from '@/services/tbApi';

// Using file upload
const result = await tbApi.predict(imageFile);
console.log(result.prediction); // "Normal" or "Tuberculosis"
console.log(result.confidence); // 0.95

// Using health check
const health = await tbApi.getHealth();
console.log(health.status); // "operational"
```

### Python

```python
import requests
import base64

# Read image file
with open('chest_xray.png', 'rb') as f:
    image_data = f.read()

# Convert to base64
image_base64 = base64.b64encode(image_data).decode('utf-8')

# Make prediction
response = requests.post(
    'http://localhost:8000/predict/tuberculosis',
    json={'image_base64': image_base64}
)

result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']}")
```

---

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` - Frontend dev server
- `http://localhost:8000` - API dev server
- `http://127.0.0.1:3000` - Local testing
- `http://127.0.0.1:8000` - Local testing
- `https://cnn-disease-detection-system-server.onrender.com` - Production

**Update CORS origins in `api.py`** for your deployment:

```python
allow_origins=[
    "your-frontend-domain.com",
    "http://localhost:3000",
]
```

---

## Image Format Support

**Supported Formats**:
- PNG (.png)
- JPEG (.jpg, .jpeg)
- GIF (.gif)
- WebP (.webp)

**Recommended**:
- Format: PNG or JPEG
- Size: 224x224 pixels (will be resized)
- Quality: Standard X-ray imaging quality

---

## Error Handling

### Common Errors

**400 Bad Request - No image data**
```json
{
  "detail": "No image data provided"
}
```

**400 Bad Request - Invalid file type**
```json
{
  "detail": "File must be an image"
}
```

**404 Not Found**
```json
{
  "detail": "Endpoint '/unknown' not found. Visit /docs for available endpoints."
}
```

**500 Internal Server Error**
```json
{
  "detail": "Error description"
}
```

---

## Performance Considerations

| Aspect | Details |
|--------|---------|
| **Timeout** | 30 seconds per request |
| **Max Image Size** | No strict limit (gzip compression used) |
| **Processing Time** | ~500ms - 2s per image |
| **Concurrency** | Handled by FastAPI (async/await) |
| **Rate Limiting** | None (implement on production) |

---

## Running the API

### 1. Prerequisites
```bash
# Python 3.8+
# Virtual environment with dependencies installed
# See requirements.txt
```

### 2. Start the Server
```bash
# From cnn_models directory
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 3. Access Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Database/Logging

Currently, the API logs:
- Prediction requests
- Model loading status
- Errors and exceptions

Consider adding:
- Request logging (timestamp, model, duration)
- Database storage for predictions
- Analytics and monitoring

---

## Security Considerations

For production deployment:

1. **CORS**: Restrict to specific domains only
2. **Authentication**: Add JWT or API key authentication
3. **Rate Limiting**: Implement request throttling
4. **Input Validation**: More strict image validation
5. **HTTPS**: Use SSL/TLS for all connections
6. **Logging**: Use proper logging framework
7. **Monitoring**: Set up alerts for errors

---

## Deployment

### Docker

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "cnn_models.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Create `.env` file:
```env
FRONTEND_URL=http://localhost:3000
API_PORT=8000
API_HOST=0.0.0.0
DEBUG=False
```

---

## Monitoring & Logging

### Health Monitoring
```bash
# Check API health
curl http://localhost:8000/health
```

### Request Logging
All requests are logged with:
- Timestamp
- Endpoint
- Status code
- Processing time

---

## Future Enhancements

- [ ] Batch prediction endpoint
- [ ] Model versioning
- [ ] Request caching
- [ ] Database integration
- [ ] User authentication
- [ ] Rate limiting
- [ ] API metrics/monitoring
- [ ] Request logging
- [ ] Webhook notifications

---

## Support

For issues or questions:
1. Check `/docs` endpoint for interactive API documentation
2. Review error messages in response
3. Check server logs for details
4. Ensure images are valid format
5. Verify CORS configuration

---

## API Changelog

### v1.0.0 (Current)
- Initial release
- 4 disease detection models
- Base64 and file upload methods
- Comprehensive documentation
- Health checks
- Model information endpoints

---

**Last Updated**: March 30, 2026  
**Status**: ✅ Production Ready
