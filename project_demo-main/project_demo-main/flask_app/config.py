import os

# Set the base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths for file uploads and outputs
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

# ChatGPT-4o Mini API Key (Replace with your actual key)
CHATGPT_API_KEY = "your_openai_api_key"

# Ensure necessary directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
