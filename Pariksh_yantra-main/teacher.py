from flask import Flask, request, render_template
import csv
import uuid
import os

app = Flask(__name__, template_folder='UI/templates')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'Database')
QUESTIONS_DIR = os.path.join(DATABASE_DIR, 'questions')
UI_DIR = os.path.join(BASE_DIR, 'UI')
TEMPLATES_DIR = os.path.join(UI_DIR, 'templates')

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(QUESTIONS_DIR, exist_ok=True)
os.makedirs(UI_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)

print(f"Database directory: {DATABASE_DIR}")
print(f"Templates directory: {TEMPLATES_DIR}")

@app.route('/')
def teacher_portal():
    return render_template('Teacher_potral.html')

@app.route('/TP_create_exam')
def index():
    return render_template('TP_create_exam.html')

@app.route('/submit_test_details', methods=['POST'])
def submit_test_details():
    try:
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        duration = request.form['duration']
        subject = request.form['subject']
        faculty = request.form['faculty']
        total_marks = request.form['total_marks']

        questions = request.form.getlist('questions')
        marks = request.form.getlist('marks')

        if not questions or not marks:
            return "Error: Questions and marks are required", 400

        unique_test_code = str(uuid.uuid4())[:8]
        exam_file_path = os.path.join(DATABASE_DIR, 'test_details.csv')
        file_exists = os.path.isfile(exam_file_path)
        # Handle optional PDF upload
        papers_dir = os.path.join(DATABASE_DIR, 'papers')
        os.makedirs(papers_dir, exist_ok=True)
        pdf_filename = ''
        if 'question_pdf' in request.files:
            pdf_file = request.files['question_pdf']
            if pdf_file and pdf_file.filename:
                # basic validation for PDF extension
                if pdf_file.filename.lower().endswith('.pdf'):
                    pdf_filename = f"{unique_test_code}_paper.pdf"
                    pdf_save_path = os.path.join(papers_dir, pdf_filename)
                    pdf_file.save(pdf_save_path)
                else:
                    return "Uploaded file must be a PDF", 400

        with open(exam_file_path, 'a', newline='', encoding='utf-8') as exam_file:
            writer = csv.writer(exam_file)
            if not file_exists or os.stat(exam_file_path).st_size == 0:
                writer.writerow(["Name", "Time", "Date", "Duration", "Subject", "Faculty Name", "Total Marks", "Unique Test Code", "Question PDF"])
            writer.writerow([name, time, date, duration, subject, faculty, total_marks, unique_test_code, pdf_filename])

        questions_file_path = os.path.join(QUESTIONS_DIR, f"{unique_test_code}_questions.csv")
        with open(questions_file_path, 'w', newline='', encoding='utf-8') as questions_file:
            writer = csv.writer(questions_file)
            writer.writerow(["Question", "Marks"])
            for q, m in zip(questions, marks):
                writer.writerow([q, m])

        return render_template('success.html', test_code=unique_test_code)

    except KeyError as e:
        return f"Missing form field: {e}", 40
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/check_directories')
def check_directories():
    directory_info = {
        'base_dir': BASE_DIR,
        'database_dir': DATABASE_DIR,
        'questions_dir': QUESTIONS_DIR,
        'templates_dir': TEMPLATES_DIR,
        'database_exists': os.path.exists(DATABASE_DIR),
        'questions_exists': os.path.exists(QUESTIONS_DIR),
        'templates_exists': os.path.exists(TEMPLATES_DIR)
    }
    return directory_info

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Directory structure:")
    print(f"Base: {BASE_DIR}")
    print(f"Database: {DATABASE_DIR}")
    print(f"Questions: {QUESTIONS_DIR}")
    print(f"Templates: {TEMPLATES_DIR}")
    app.run(debug=True, host='0.0.0.0', port=5000)