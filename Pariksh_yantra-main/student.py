import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
question_folder = os.path.join(BASE_DIR, "Database", "question")
csv_file_path = os.path.join(BASE_DIR, "Database", "test_details.csv")
student_csv_file_path = os.path.join(BASE_DIR, "Database", "student_details.csv")
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import csv

app = Flask(__name__, template_folder='UI/templates')
app.secret_key = 'AIzaSyDfTuvXd7_FkmPWYEsqKPoni4F3n65_vRk' 


# Folder path where the question CSV files are stored
questions_folder = os.path.join(BASE_DIR, "Database", "questions")

# CSV file path for test details (use absolute path)
# Already set above as csv_file_path and student_csv_file_path

# Function to check if the test code exists in the CSV
def is_code_valid(test_code):
    try:
        # Read using csv.DictReader to tolerate multiple header rows and inconsistent column names
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # For each row, try to find any column that looks like the unique code column
                for k, v in row.items():
                    if k is None:
                        continue
                    key = k.strip().lower()
                    if 'unique' in key or 'test code' in key or 'code' in key:
                        if v is not None and str(v).strip() == str(test_code).strip():
                            return True
        return False
    except Exception as e:
        print(f"Error reading CSV file in is_code_valid: {e}")
        return False

# Function to search and load test details based on test code
def get_test_details(test_code):
    test_details = {}
    try:
        # Open CSV and search rows for the matching test code with flexible header matching
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Find the key in this row that represents the test code
                code_found = False
                for k, v in row.items():
                    if k is None:
                        continue
                    key = k.strip().lower()
                    if 'unique' in key or 'test code' in key or 'code' in key:
                        if v is not None and str(v).strip() == str(test_code).strip():
                            code_found = True
                            break
                if not code_found:
                    continue

                # Helper to get a field value by searching keys for keywords
                def get_field(row, keywords, default='N/A'):
                    for kk, vv in row.items():
                        if kk is None:
                            continue
                        nkk = kk.strip().lower()
                        for kw in keywords:
                            if kw in nkk:
                                return vv if vv is not None else default
                    return default

                test_details['name'] = get_field(row, ['name'])
                test_details['time'] = get_field(row, ['time'])
                test_details['date'] = get_field(row, ['date'])
                test_details['duration'] = get_field(row, ['duration'])
                test_details['subject'] = get_field(row, ['subject'])
                test_details['faculty'] = get_field(row, ['faculty', 'faculty name'])
                test_details['total_marks'] = get_field(row, ['total', 'marks'])
                break
    except Exception as e:
        print(f"Error fetching test details: {e}")
    return test_details

# Function to load questions based on test code
def load_questions(test_code):
    file_name = f"{test_code}_questions.csv"
    file_path = os.path.join(questions_folder, file_name)
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            required_columns = ['Question', 'Marks']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                print(f"Error: Missing columns in {file_name}: {missing}. Found columns: {df.columns.tolist()}")
                return None
            return df[required_columns].to_dict(orient='records')
        except Exception as e:
            print(f"Error reading the questions file: {e}")
            return None
    else:
        print(f"Questions file not found: {file_path}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_code = request.form['test_code']
        if is_code_valid(test_code):
            session['test_code'] = test_code
            return redirect(url_for('student_login'))
        else:
            return render_template('Student_test_check.html', error="Enter a valid test code.")
    return render_template('Student_test_check.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        email = request.form['email']
        unique_code = session.get('test_code', None)

        try:
            with open(student_csv_file_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if os.stat(student_csv_file_path).st_size == 0:
                    writer.writerow(['Name', 'Roll Number', 'Email ID', 'Unique Code'])
                writer.writerow([name, roll_number, email, unique_code])
        except Exception as e:
            print(f"Error saving student details: {e}")
        
        return redirect(url_for('test_instruction'))
    test_code = session.get('test_code', None)
    return render_template('Student_login_details.html', test_code=test_code)

@app.route('/test_instruction', methods=['GET', 'POST'])
def test_instruction():
    if request.method == 'POST':
        return redirect(url_for('student_test_portal', test_code=session.get('test_code')))
    return render_template('Student_test_instruction.html')

@app.route('/student_test_portal/<test_code>', methods=['GET'])
def student_test_portal(test_code):
    test_details = get_test_details(test_code)
    question = load_questions(test_code)
    if test_details and question:
        return render_template('Student_test_potral.html', test_details=test_details, questions=question)
    else:
        return "Test details or questions not found"
@app.route('/submit', methods=['POST'])
def submit():
    # You can handle any form data here if needed
    return render_template('Student_test_submit.html')
if __name__ == '__main__':
    app.run(debug=True)