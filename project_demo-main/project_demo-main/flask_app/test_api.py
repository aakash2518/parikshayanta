#!/usr/bin/env python3
"""
API Test Script for Flask OCR Evaluation App
"""

import requests
import json
import os
from pathlib import Path

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print("\nTesting status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_upload(question_file_path=None, answer_file_path=None):
    """Test file upload endpoint"""
    print("\nTesting upload endpoint...")
    
    if not question_file_path or not answer_file_path:
        print("No file paths provided. Skipping upload test.")
        print("To test upload, provide file paths:")
        print("test_upload('path/to/question.pdf', 'path/to/answer.pdf')")
        return False
    
    try:
        files = {
            'question_paper': open(question_file_path, 'rb'),
            'answer_sheet': open(answer_file_path, 'rb')
        }
        
        response = requests.post(f"{BASE_URL}/upload", files=files)
        
        # Close files
        files['question_paper'].close()
        files['answer_sheet'].close()
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_process():
    """Test process endpoint"""
    print("\nTesting process endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/process")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_results(filename="extracted_data.xlsx"):
    """Test results endpoint"""
    print(f"\nTesting results endpoint for {filename}...")
    try:
        response = requests.get(f"{BASE_URL}/results/{filename}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            if data.get('success'):
                results = data.get('data', {}).get('results', [])
                print(f"Total questions: {len(results)}")
                if results:
                    print("First result:")
                    print(json.dumps(results[0], indent=2))
        else:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_download(filename="extracted_data.xlsx"):
    """Test download endpoint"""
    print(f"\nTesting download endpoint for {filename}...")
    try:
        response = requests.get(f"{BASE_URL}/download/{filename}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"File size: {len(response.content)} bytes")
            print("Download successful!")
        else:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests(question_file=None, answer_file=None):
    """Run all API tests"""
    print("=" * 50)
    print("API Test Suite")
    print("=" * 50)
    
    results = {}
    
    # Test basic endpoints
    results['health'] = test_health()
    results['status'] = test_status()
    
    # Test upload if files provided
    if question_file and answer_file:
        results['upload'] = test_upload(question_file, answer_file)
        if results['upload']:
            results['process'] = test_process()
            if results['process']:
                results['results'] = test_results()
                results['download'] = test_download()
    else:
        print("\nSkipping upload, process, results, and download tests.")
        print("To test these endpoints, provide PDF file paths:")
        print("run_all_tests('question.pdf', 'answer.pdf')")
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Results Summary:")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_name.upper()}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")

if __name__ == "__main__":
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("Server is running!")
    except:
        print("Error: Server is not running!")
        print("Please start the Flask app first: python app.py")
        exit(1)
    
    # Run tests
    run_all_tests()
    
    print("\nTo test with actual PDF files:")
    print("python test_api.py")
    print("Then call: run_all_tests('path/to/question.pdf', 'path/to/answer.pdf')")