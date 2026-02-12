from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import config
from ocr import process_pdfs
from evaluation import evaluate_answers
import pandas as pd
from datetime import datetime

app = Flask(__name__, static_folder="static")
CORS(app)  # Enable CORS for API access

app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = config.OUTPUT_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

@app.route("/")
def index():
    return render_template("index.html")

# API Routes
@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route("/api/upload", methods=["POST"])
def api_upload_files():
    """API endpoint to upload question paper and answer sheet"""
    try:
        question_paper = request.files.get("question_paper")
        answer_sheet = request.files.get("answer_sheet")

        if not question_paper or not answer_sheet:
            return jsonify({
                "success": False,
                "error": "Both question_paper and answer_sheet files are required"
            }), 400

        # Validate file types
        allowed_extensions = {'pdf'}
        if not (question_paper.filename.lower().endswith('.pdf') and 
                answer_sheet.filename.lower().endswith('.pdf')):
            return jsonify({
                "success": False,
                "error": "Only PDF files are allowed"
            }), 400

        # Generate unique filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        q_filename = f"question_paper_{timestamp}.pdf"
        a_filename = f"answer_sheet_{timestamp}.pdf"
        
        q_path = os.path.join(app.config["UPLOAD_FOLDER"], q_filename)
        a_path = os.path.join(app.config["UPLOAD_FOLDER"], a_filename)

        question_paper.save(q_path)
        answer_sheet.save(a_path)

        return jsonify({
            "success": True,
            "message": "Files uploaded successfully",
            "data": {
                "question_paper": q_filename,
                "answer_sheet": a_filename,
                "upload_time": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Upload failed: {str(e)}"
        }), 500

@app.route("/api/process", methods=["POST"])
def api_process():
    """API endpoint to process uploaded PDFs and generate evaluation"""
    try:
        # Check if files exist
        q_path = os.path.join(app.config["UPLOAD_FOLDER"], "question_paper.pdf")
        a_path = os.path.join(app.config["UPLOAD_FOLDER"], "answer_sheet.pdf")
        
        if not (os.path.exists(q_path) and os.path.exists(a_path)):
            return jsonify({
                "success": False,
                "error": "Please upload both question paper and answer sheet first"
            }), 400

        # Process PDFs
        excel_path = process_pdfs()
        doc_path = evaluate_answers(excel_path)
        
        # Get file names for download
        excel_filename = os.path.basename(excel_path)
        doc_filename = os.path.basename(doc_path)

        return jsonify({
            "success": True,
            "message": "Processing completed successfully",
            "data": {
                "excel_file": excel_filename,
                "doc_file": doc_filename,
                "excel_download_url": f"/api/download/{excel_filename}",
                "doc_download_url": f"/api/download/{doc_filename}",
                "processed_time": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Processing failed: {str(e)}"
        }), 500

@app.route("/api/download/<filename>", methods=["GET"])
def api_download_file(filename):
    """API endpoint to download generated files"""
    try:
        file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        
        return jsonify({
            "success": False,
            "error": "File not found"
        }), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Download failed: {str(e)}"
        }), 500

@app.route("/api/status", methods=["GET"])
def api_status():
    """Get processing status and available files"""
    try:
        upload_files = []
        output_files = []
        
        # Check upload folder
        if os.path.exists(app.config["UPLOAD_FOLDER"]):
            upload_files = [f for f in os.listdir(app.config["UPLOAD_FOLDER"]) 
                          if f.endswith('.pdf')]
        
        # Check output folder
        if os.path.exists(app.config["OUTPUT_FOLDER"]):
            output_files = [f for f in os.listdir(app.config["OUTPUT_FOLDER"]) 
                          if f.endswith(('.xlsx', '.docx'))]

        return jsonify({
            "success": True,
            "data": {
                "uploaded_files": upload_files,
                "output_files": output_files,
                "upload_folder_exists": os.path.exists(app.config["UPLOAD_FOLDER"]),
                "output_folder_exists": os.path.exists(app.config["OUTPUT_FOLDER"]),
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Status check failed: {str(e)}"
        }), 500

@app.route("/api/results/<filename>", methods=["GET"])
def api_get_results(filename):
    """Get evaluation results as JSON"""
    try:
        file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
        
        if not os.path.exists(file_path):
            return jsonify({
                "success": False,
                "error": "Results file not found"
            }), 404

        if filename.endswith('.xlsx'):
            # Read Excel file and return as JSON
            df = pd.read_excel(file_path)
            results = df.to_dict('records')
            
            return jsonify({
                "success": True,
                "data": {
                    "results": results,
                    "total_questions": len(results),
                    "filename": filename
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "Only Excel files can be returned as JSON"
            }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get results: {str(e)}"
        }), 500

# Legacy routes (for backward compatibility)
@app.route("/upload", methods=["POST"])
def upload_files():
    question_paper = request.files.get("question_paper")
    answer_sheet = request.files.get("answer_sheet")

    if not question_paper or not answer_sheet:
        return jsonify({"error": "Both files are required!"}), 400

    q_path = os.path.join(app.config["UPLOAD_FOLDER"], "question_paper.pdf")
    a_path = os.path.join(app.config["UPLOAD_FOLDER"], "answer_sheet.pdf")

    question_paper.save(q_path)
    answer_sheet.save(a_path)

    return jsonify({"message": "Files uploaded successfully!"})

@app.route("/process", methods=["POST"])
def process():
    try:
        excel_path = process_pdfs()
        doc_path = evaluate_answers(excel_path)
        return jsonify({"message": "Processing completed!", "excel": excel_path, "doc": doc_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(app.config["OUTPUT_FOLDER"], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
