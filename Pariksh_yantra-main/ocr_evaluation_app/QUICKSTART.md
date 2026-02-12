# Quick Start Guide - OCR Evaluation App

Get up and running with the OCR Evaluation App in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation

1. **Navigate to the app directory:**
   ```bash
   cd ocr_evaluation_app
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   
   **Option 1 - Environment Variable (Recommended):**
   ```bash
   # On Windows (CMD):
   set OPENAI_API_KEY=your-api-key-here
   
   # On Windows (PowerShell):
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # On macOS/Linux:
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   **Option 2 - Edit config.py:**
   Open `config.py` and replace `'your_openai_api_key'` with your actual API key.

## Running the App

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Access the web interface:**
   Open your browser and go to: `http://localhost:5000`

3. **Upload and process:**
   - Upload a question paper PDF
   - Upload an answer sheet PDF
   - Click "Submit for OCR & Evaluation"
   - Download the generated Excel and Word reports

## Using the API

### Quick Test

```bash
# Check if the API is running
curl http://localhost:5000/api/health
```

### Upload and Process

```bash
# Upload PDFs
curl -X POST \
  -F "question_paper=@your_question.pdf" \
  -F "answer_sheet=@your_answer.pdf" \
  http://localhost:5000/api/upload

# Process the files
curl -X POST http://localhost:5000/api/process

# Download results
curl -O http://localhost:5000/api/download/extracted_data.xlsx
curl -O http://localhost:5000/api/download/evaluation.docx
```

### Using Python

```python
from api_client_example import OCREvaluationClient

client = OCREvaluationClient()
client.complete_workflow('question.pdf', 'answer.pdf')
```

## Testing

Run the test suite:
```bash
python test_api.py
```

## Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:** Make sure you've set the `OPENAI_API_KEY` environment variable or updated `config.py`

### Issue: "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Port 5000 already in use"
**Solution:** Either stop the other service using port 5000, or modify `app.py` to use a different port:
```python
app.run(debug=True, port=5001)
```

### Issue: "PDF extraction failed"
**Solution:** Ensure your PDF files are not corrupted and contain readable text (not just images)

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference
- Explore [api_client_example.py](api_client_example.py) for programmatic usage examples

## Project Structure

```
ocr_evaluation_app/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── ocr.py                    # OCR processing logic
├── evaluation.py             # AI evaluation logic
├── utils.py                  # Utility functions
├── requirements.txt          # Python dependencies
├── API_DOCUMENTATION.md      # Complete API reference
├── api_client_example.py     # Example Python client
├── test_api.py              # API test suite
├── static/                   # CSS and JavaScript files
├── templates/                # HTML templates
├── uploads/                  # Temporary PDF storage
├── output/                   # Generated Excel/Word files
└── results/                  # Evaluation results
```

## Support

For issues or questions:
1. Check the [README.md](README.md) for detailed documentation
2. Review the [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. Run tests with `python test_api.py` to diagnose issues

Happy evaluating! 🎉
