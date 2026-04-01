# Backend Setup Guide

## Starting the Backend API

### Quick Start

**1. Navigate to cnn_models directory**:
```bash
cd cnn_models
```

**2. Start the API server**:
```bash
# Using Python directly
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

# Or using uvicorn command
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**3. Verify it's running**:
```bash
# In another terminal
curl http://localhost:8000/health
```

**Expected output**:
```json
{
  "status": "operational",
  "message": "API is running"
}
```

---

## API Endpoints Overview

### Base URL: `http://localhost:8000`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/` | API info |
| GET | `/info/models` | Available models |
| POST | `/predict/tuberculosis` | TB prediction (base64) |
| POST | `/predict/tuberculosis/file` | TB prediction (file) |
| POST | `/predict/pneumonia` | Pneumonia prediction |
| POST | `/predict/bone_fracture` | Bone fracture prediction |
| POST | `/predict/lung_cancer` | Lung cancer prediction |

---

## Frontend Configuration

**Update `.env` in client directory**:
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## Testing the API

### Using Swagger UI
1. Open browser: `http://localhost:8000/docs`
2. Try out endpoints interactively
3. Upload test images
4. See responses in real-time

### Using ReDoc
1. Open browser: `http://localhost:8000/redoc`
2. View complete API documentation
3. See all endpoints and schemas

### Using cURL

**Test health**:
```bash
curl http://localhost:8000/health
```

**Test TB prediction with file**:
```bash
curl -X POST "http://localhost:8000/predict/tuberculosis/file" \
  -F "file=@path/to/chest_xray.png"
```

**Test TB prediction with base64** (from frontend):
```bash
# See API_DOCUMENTATION.md for examples
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port
python -m uvicorn api:app --host 0.0.0.0 --port 8001

# Or kill existing process
# On Windows: netstat -ano | findstr :8000
# On Mac/Linux: lsof -i :8000 | kill -9 <PID>
```

### Module Not Found Errors
```bash
# Make sure you're in cnn_models directory
cd cnn_models

# Install requirements
pip install -r requirements.txt

# Then start server
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### CORS Errors in Frontend
- Check CORS origins in `api.py`
- Update to include your frontend URL
- Restart the server

### 404 on API Endpoints
- Verify base URL in frontend `.env`
- Check API is running
- Visit `/docs` to see available endpoints

---

## Development vs Production

### Development
```bash
python -m uvicorn api:app \
  --host 127.0.0.1 \
  --port 8000 \
  --reload
```

Benefits:
- Auto-reload on code changes
- Debug mode enabled
- Dev-only CORS settings

### Production
```bash
python -m uvicorn api:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4
```

Changes needed:
- Remove `--reload` flag
- Add `--workers` for concurrency
- Update CORS origins
- Enable SSL/HTTPS
- Set up logging

---

## Running Both Services

### Terminal 1 - Frontend
```bash
cd client
pnpm start
# Runs on http://localhost:3000
```

### Terminal 2 - Backend
```bash
cd cnn_models
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
# Runs on http://localhost:8000
```

### Terminal 3 - Optional (Testing)
```bash
# Run test requests
curl http://localhost:8000/health
```

---

## API Features

✅ **Disease Detection**
- Tuberculosis
- Pneumonia
- Bone fractures
- Lung cancer

✅ **Input Methods**
- Base64 encoded images (JSON)
- File uploads (FormData)

✅ **Response Data**
- Prediction label
- Confidence score (0-1)
- Grad-CAM heatmap
- Model information

✅ **Production Features**
- CORS enabled
- Error handling
- Request validation
- Health checks
- API documentation

---

## Image Conversion Flow

### Frontend to Backend
```
User selects image file
         ↓
imageUtils.fileToBase64()
         ↓
Base64 string
         ↓
Send to API in JSON
         ↓
Backend processes
```

### Backend Response
```
Model prediction
         ↓
Create heatmap
         ↓
Confidence score
         ↓
Return base64 heatmap
         ↓
Frontend receives
         ↓
imageUtils.base64ToDataUrl()
         ↓
Display heatmap in UI
```

---

## Available Commands

### Start Server
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Check Health
```bash
curl http://localhost:8000/health
```

### Get API Info
```bash
curl http://localhost:8000/
```

### Get Models Info
```bash
curl http://localhost:8000/info/models
```

### Open API Docs
```
Visit: http://localhost:8000/docs
```

---

## Next Steps

1. ✅ Start backend: `python -m uvicorn api:app --port 8000 --reload`
2. ✅ Start frontend: `pnpm start` (in client directory)
3. ✅ Open http://localhost:3000
4. ✅ Upload test chest X-ray
5. ✅ See TB prediction
6. ✅ View heatmap visualization

---

## Performance Notes

| Aspect | Spec |
|--------|------|
| **Prediction Time** | ~500ms - 2s per image |
| **Timeout** | 30 seconds |
| **Concurrent Requests** | Unlimited (FastAPI async) |
| **Image Size** | No strict limit |
| **Supported Formats** | PNG, JPG, JPEG, GIF, WebP |

---

## Environment Variables

Optional - edit in `api.py`:
```python
API_PORT = os.getenv("API_PORT", 8000)
DEBUG = os.getenv("DEBUG", "True")
```

---

## Full System Architecture

```
Frontend (React)
    ↓
Redux Store
    ↓
Image Utils (fileToBase64)
    ↓
API Service (axios)
    ↓
Backend FastAPI
    ↓
Disease Detection Models
    ↓
Response with Heatmap
    ↓
Display Results
```

---

## Useful Resources

- **API Docs**: http://localhost:8000/docs
- **Backend Code**: `cnn_models/api.py`
- **Frontend Code**: `client/src/services/tbApi.ts`
- **Image Utils**: `client/src/utils/imageUtils.ts`
- **API Documentation**: `cnn_models/API_DOCUMENTATION.md`

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change port or kill process |
| Module not found | `pip install -r requirements.txt` |
| CORS error | Update CORS in api.py |
| 404 on endpoint | Check /docs for correct endpoints |
| Model not loading | Verify pth files exist in pth_files/ |

---

**Status**: ✅ API Ready to Use  
**Last Updated**: March 30, 2026
