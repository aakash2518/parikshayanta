#!/usr/bin/env python3
"""
Example API Client for Flask OCR Evaluation App
This shows how to interact with the API programmatically.
"""

import requests
import json
import time
import os

class OCREvaluationClient:
    def __init__(self, base_url="http://localhost:5000/api"):
        self.base_url = base_url
        
    def health_check(self):
        """Check if API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Health check failed: {e}")
            return None
    
    def upload_files(self, question_pdf_path, answer_pdf_path):
        """Upload question paper and answer sheet"""
        try:
            with open(question_pdf_path, 'rb') as q_file, open(answer_pdf_path, 'rb') as a_file:
                files = {
                    'question_paper': q_file,
                    'answer_sheet': a_file
                }
                response = requests.post(f"{self.base_url}/upload", files=files)
                return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Upload failed: {e}")
            return None
    
    def process_files(self):
        """Process uploaded files"""
        try:
            response = requests.post(f"{self.base_url}/process")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Processing failed: {e}")
            return None
    
    def get_status(self):
        """Get current status"""
        try:
            response = requests.get(f"{self.base_url}/status")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Status check failed: {e}")
            return None
    
    def get_results(self, filename="extracted_data.xlsx"):
        """Get results as JSON"""
        try:
            response = requests.get(f"{self.base_url}/results/{filename}")
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Get results failed: {e}")
            return None
    
    def download_file(self, filename, save_path=None):
        """Download a file"""
        try:
            response = requests.get(f"{self.base_url}/download/{filename}")
            if response.status_code == 200:
                if save_path is None:
                    save_path = filename
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"Download failed: {e}")
            return False
    
    def complete_workflow(self, question_pdf, answer_pdf, download_dir="downloads"):
        """Complete workflow: upload -> process -> download results"""
        print("Starting complete OCR evaluation workflow...")
        
        # 1. Health check
        print("1. Checking API health...")
        health = self.health_check()
        if not health:
            print("❌ API is not healthy!")
            return False
        print(f"✅ API is healthy (version: {health.get('version')})")
        
        # 2. Upload files
        print("2. Uploading files...")
        upload_result = self.upload_files(question_pdf, answer_pdf)
        if not upload_result or not upload_result.get('success'):
            print("❌ Upload failed!")
            return False
        print("✅ Files uploaded successfully")
        
        # 3. Process files
        print("3. Processing files...")
        process_result = self.process_files()
        if not process_result or not process_result.get('success'):
            print("❌ Processing failed!")
            return False
        print("✅ Processing completed")
        
        # 4. Get results
        print("4. Getting results...")
        results = self.get_results()
        if results and results.get('success'):
            data = results.get('data', {})
            print(f"✅ Found {data.get('total_questions', 0)} questions")
            
            # Print first result as example
            if data.get('results'):
                first_result = data['results'][0]
                print(f"Example result: Q{first_result.get('Question No.')}: {first_result.get('Marks', 'N/A')}")
        
        # 5. Download files
        print("5. Downloading files...")
        os.makedirs(download_dir, exist_ok=True)
        
        data = process_result.get('data', {})
        excel_file = data.get('excel_file')
        doc_file = data.get('doc_file')
        
        downloaded = 0
        if excel_file:
            if self.download_file(excel_file, os.path.join(download_dir, excel_file)):
                print(f"✅ Downloaded {excel_file}")
                downloaded += 1
        
        if doc_file:
            if self.download_file(doc_file, os.path.join(download_dir, doc_file)):
                print(f"✅ Downloaded {doc_file}")
                downloaded += 1
        
        print(f"\n🎉 Workflow completed! Downloaded {downloaded} files to '{download_dir}' folder")
        return True

def main():
    """Example usage"""
    client = OCREvaluationClient()
    
    # Example file paths (update these with your actual PDF files)
    question_pdf = "sample_question.pdf"
    answer_pdf = "sample_answer.pdf"
    
    # Check if example files exist
    if not (os.path.exists(question_pdf) and os.path.exists(answer_pdf)):
        print("Example PDF files not found!")
        print("Please update the file paths in the script or create sample PDFs:")
        print(f"- {question_pdf}")
        print(f"- {answer_pdf}")
        print("\nAlternatively, you can call the methods individually:")
        print("client = OCREvaluationClient()")
        print("client.health_check()")
        print("client.get_status()")
        return
    
    # Run complete workflow
    success = client.complete_workflow(question_pdf, answer_pdf)
    
    if success:
        print("\n✅ All done! Check the 'downloads' folder for your results.")
    else:
        print("\n❌ Workflow failed. Check the error messages above.")

if __name__ == "__main__":
    main()