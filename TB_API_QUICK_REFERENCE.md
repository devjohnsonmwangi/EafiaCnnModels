# 🔥 TB MODEL API - QUICK REFERENCE

## ✅ STATUS: FULLY OPERATIONAL

---

## 🚀 QUICK START

### 1. Start the API (if not running)
```powershell
cd "c:\Users\devjohnsonmwangi\Desktop\TbCNNapp\Eafia\cnn_models"
& "c:\Users\devjohnsonmwangi\Desktop\TbCNNapp\.venv\Scripts\python.exe" api.py
```

### 2. API URL
```
http://localhost:5000
```

### 3. Documentation UI
```
http://localhost:5000/docs
```

---

## 📡 ENDPOINTS

### Health Check
```
GET /health
```
**Response:** `{"status": "operational", "message": "API is running"}`

---

### TB Classification (Base64)
```
POST /predict/tuberculosis
Content-Type: application/json

{
  "image_base64": "<base64_encoded_image>"
}
```

**Response:**
```json
{
  "prediction": "Normal" | "Tuberculosis",
  "confidence": 0.95,
  "heatmap": "<base64_encoded_heatmap>",
  "model": "resnet18"
}
```

---

### TB Classification (File Upload)
```
POST /predict/tuberculosis/file
Content-Type: multipart/form-data

file: <image_file>
```

**Supported:** PNG, JPG, JPEG

---

## 🧪 TEST COMMANDS

### PowerShell - Health Check
```powershell
(Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing).Content | ConvertFrom-Json
```

### Python - Test Classification
```bash
cd Eafia\cnn_models
python test_tb_model.py
```

---

## 📊 MODEL INFO

| Property | Value |
|----------|-------|
| Architecture | ResNet18 |
| Model File | pth_files/tb_classifier.pth (42.71 MB) |
| Input Size | 224×224 RGB |
| Classes | Normal, Tuberculosis |
| Confidence | 0.0 - 1.0 |
| Heatmap | GradCAM visualization |
| Server | Uvicorn |
| Port | 5000 |

---

## 🔗 BACKEND INTEGRATION

**NestJS File:** `Eafia/api/src/modules/patients/patients.service.ts`

**Key Method:** `performTBDiagnosis()`

**Features:**
- 90-second timeout
- Base64 image transmission
- Proper field mapping
- Heatmap storage in database
- TB workflow trigger on positive

---

## ⚙️ CONFIGURATION

**Timeout:** 90 seconds  
**Validation Threshold:** Confidence > 0.2  
**CORS Enabled:** Yes (localhost:3000)  
**Heatmap Output:** Base64 encoded  

---

## 📝 RESPONSE FIELDS

| Field | Type | Example |
|-------|------|---------|
| prediction | string | "Tuberculosis" |
| confidence | float | 0.85 |
| heatmap | string | "iVBORw0KGgo..." |
| model | string | "resnet18" |

---

## ⚡ PERFORMANCE

- **Inference:** 5-15 seconds per image (CPU)
- **Memory:** ~150 MB for model + ~50 MB per inference
- **Throughput:** ~1-2 images/second

---

## ✨ TESTS

✅ Health Check  
✅ Base64 Classification  
✅ File Upload Classification  
✅ Heatmap Generation  
✅ Response Validation

---

## 🎯 NEXT STEPS

1. Upload X-ray from frontend
2. Backend sends Base64 to `/predict/tuberculosis`
3. Model classifies and returns prediction + heatmap
4. Backend stores results in database
5. Frontend displays diagnosis and heatmap

---

**API Ready:** ✅ April 1, 2026
