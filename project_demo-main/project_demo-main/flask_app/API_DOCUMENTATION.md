# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### 1. Health Check
**GET** `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-11T10:30:00",
  "version": "1.0.0"
}
```

### 2. Upload Files
**POST** `/api/upload`

Upload question paper and answer sheet PDFs.

**Request:**
- Content-Type: `multipart/form-data`
- Files:
  - `question_paper`: PDF file
  - `answer_sheet`: PDF file

**Response:**
```json
{
  "success": true,
  "message": "Files uploaded successfully",
  "data": {
    "question_paper": "question_paper_20240111_103000.pdf",
    "answer_sheet": "answer_sheet_20240111_103000.pdf",
    "upload_time": "2024-01-11T10:30:00"
  }
}
```

### 3. Process Files
**POST** `/api/process`

Process uploaded PDFs and generate evaluation.

**Response:**
```json
{
  "success": true,
  "message": "Processing completed successfully",
  "data": {
    "excel_file": "extracted_data.xlsx",
    "doc_file": "evaluation.docx",
    "excel_download_url": "/api/download/extracted_data.xlsx",
    "doc_download_url": "/api/download/evaluation.docx",
    "processed_time": "2024-01-11T10:35:00"
  }
}
```

### 4. Download Files
**GET** `/api/download/{filename}`

Download generated files.

**Parameters:**
- `filename`: Name of the file to download

**Response:**
- File download or error message

### 5. Get Status
**GET** `/api/status`

Get current status and available files.

**Response:**
```json
{
  "success": true,
  "data": {
    "uploaded_files": ["question_paper.pdf", "answer_sheet.pdf"],
    "output_files": ["extracted_data.xlsx", "evaluation.docx"],
    "upload_folder_exists": true,
    "output_folder_exists": true,
    "timestamp": "2024-01-11T10:30:00"
  }
}
```

### 6. Get Results as JSON
**GET** `/api/results/{filename}`

Get evaluation results as JSON (only for Excel files).

**Parameters:**
- `filename`: Name of the Excel file

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "Question No.": 1,
        "Question": "What is Python?",
        "Answer": "Python is a programming language",
        "Feedback": "Good answer",
        "Marks": "8/10"
      }
    ],
    "total_questions": 1,
    "filename": "extracted_data.xlsx"
  }
}
```

## Error Responses

All endpoints return errors in this format:
```json
{
  "success": false,
  "error": "Error message description"
}
```

## Usage Examples

### Using curl

1. **Health Check:**
```bash
curl http://localhost:5000/api/health
```

2. **Upload Files:**
```bash
curl -X POST \
  -F "question_paper=@question.pdf" \
  -F "answer_sheet=@answer.pdf" \
  http://localhost:5000/api/upload
```

3. **Process Files:**
```bash
curl -X POST http://localhost:5000/api/process
```

4. **Get Status:**
```bash
curl http://localhost:5000/api/status
```

5. **Download File:**
```bash
curl -O http://localhost:5000/api/download/extracted_data.xlsx
```

### Using JavaScript (Fetch API)

```javascript
// Upload files
const formData = new FormData();
formData.append('question_paper', questionFile);
formData.append('answer_sheet', answerFile);

fetch('/api/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Process files
fetch('/api/process', {
  method: 'POST'
})
.then(response => response.json())
.then(data => console.log(data));

// Get status
fetch('/api/status')
.then(response => response.json())
.then(data => console.log(data));
```

## Legacy Endpoints (Backward Compatibility)

The following endpoints are maintained for backward compatibility:
- `POST /upload`
- `POST /process`
- `GET /download/{filename}`

## Notes

- Maximum file size: 16MB
- Only PDF files are accepted for upload
- CORS is enabled for cross-origin requests
- All API responses include proper HTTP status codes
- Timestamps are in ISO format