# OCR Evaluation Flask App

A Flask web application that processes PDF question papers and answer sheets using OCR, then evaluates answers using OpenAI's GPT model.

## Features

- **PDF Upload**: Upload question papers and answer sheets
- **OCR Processing**: Extract text from PDFs using PyMuPDF
- **AI Evaluation**: Evaluate answers using OpenAI GPT-4o-mini
- **Export Results**: Generate Excel and Word document reports
- **REST API**: Complete API for programmatic access
- **Web Interface**: User-friendly web interface

## API Endpoints

The application provides a comprehensive REST API:

### Core Endpoints
- `GET /api/health` - Health check
- `POST /api/upload` - Upload PDF files
- `POST /api/process` - Process uploaded files
- `GET /api/status` - Get current status
- `GET /api/results/{filename}` - Get results as JSON
- `GET /api/download/{filename}` - Download generated files

### Legacy Endpoints (Backward Compatible)
- `POST /upload` - Legacy upload endpoint
- `POST /process` - Legacy process endpoint
- `GET /download/{filename}` - Legacy download endpoint

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd flask_app
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure OpenAI API**
Edit `config.py` and add your OpenAI API key:
```python
CHATGPT_API_KEY = "your_actual_openai_api_key_here"
```

## Usage

### Running the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Upload question paper and answer sheet PDFs
3. Click process to analyze and evaluate
4. Download the generated Excel and Word reports

### API Usage

#### Using curl

```bash
# Health check
curl http://localhost:5000/api/health

# Upload files
curl -X POST \
  -F "question_paper=@question.pdf" \
  -F "answer_sheet=@answer.pdf" \
  http://localhost:5000/api/upload

# Process files
curl -X POST http://localhost:5000/api/process

# Get status
curl http://localhost:5000/api/status

# Download results
curl -O http://localhost:5000/api/download/extracted_data.xlsx
```

#### Using Python

```python
import requests

# Upload files
files = {
    'question_paper': open('question.pdf', 'rb'),
    'answer_sheet': open('answer.pdf', 'rb')
}
response = requests.post('http://localhost:5000/api/upload', files=files)

# Process files
response = requests.post('http://localhost:5000/api/process')

# Get results
response = requests.get('http://localhost:5000/api/results/extracted_data.xlsx')
results = response.json()
```

### Example Client

Use the provided example client for a complete workflow:

```python
from api_client_example import OCREvaluationClient

client = OCREvaluationClient()
client.complete_workflow('question.pdf', 'answer.pdf')
```

## Testing

### API Testing

Run the test suite:
```bash
python test_api.py
```

For testing with actual PDF files:
```python
from test_api import run_all_tests
run_all_tests('question.pdf', 'answer.pdf')
```

## File Structure

```
flask_app/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── ocr.py                # OCR processing logic
├── evaluation.py         # AI evaluation logic
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── API_DOCUMENTATION.md  # Detailed API docs
├── test_api.py          # API test suite
├── api_client_example.py # Example API client
├── static/              # Static files (CSS, JS)
├── templates/           # HTML templates
├── uploads/             # Uploaded PDF files
└── output/              # Generated reports
```

## Configuration

### Environment Variables

You can also set configuration via environment variables:

```bash
export OPENAI_API_KEY="your_api_key"
export UPLOAD_FOLDER="/path/to/uploads"
export OUTPUT_FOLDER="/path/to/output"
```

### API Configuration

- **CORS**: Enabled for cross-origin requests
- **File Size Limit**: 16MB maximum
- **Supported Formats**: PDF only
- **Rate Limiting**: None (add if needed for production)

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **OpenAI**: AI evaluation
- **PyMuPDF**: PDF text extraction
- **Pandas**: Data processing
- **python-docx**: Word document generation
- **Requests**: HTTP client (for testing)

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error description"
}
```

Common error codes:
- `400`: Bad request (missing files, invalid format)
- `404`: File not found
- `500`: Server error (processing failure)

## Security Considerations

- **File Validation**: Only PDF files accepted
- **File Size Limits**: 16MB maximum
- **Path Traversal**: Protected against directory traversal
- **API Key**: Keep OpenAI API key secure

## Production Deployment

For production deployment:

1. **Use a production WSGI server** (Gunicorn, uWSGI)
2. **Set up reverse proxy** (Nginx, Apache)
3. **Configure environment variables**
4. **Add rate limiting**
5. **Set up logging**
6. **Use HTTPS**

Example with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is valid and has sufficient credits
   - Check the key is properly set in `config.py`

2. **File Upload Issues**
   - Verify file is a valid PDF
   - Check file size is under 16MB
   - Ensure upload directory has write permissions

3. **Processing Errors**
   - Check if both files are uploaded
   - Verify PDF files are not corrupted
   - Check OpenAI API connectivity

### Debug Mode

Run with debug mode for detailed error messages:
```python
app.run(debug=True)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]
