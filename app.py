from datetime import datetime
from dotenv import load_dotenv
from flask import flash, Flask, render_template, request, redirect, send_from_directory
from helpers import validate_department_subject, validate_exam, validate_semester, validate_year, allowed_file
from werkzeug.utils import secure_filename
import os
import requests
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5MB
RECAPTCHA_SECRET = os.getenv('RECAPTCHA_SECRET')
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()
# Generate secret key for flash
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Connect to DB
def get_db_connection():
    conn = sqlite3.connect('pyqs.db')
    conn.row_factory = sqlite3.Row
    return conn

# Landing page
@app.route('/')
def index():
    conn = get_db_connection()
    # Render the verified pyqs on the carousel for better UX
    pyqs = conn.execute(''' SELECT * FROM pyqs WHERE verified = 1; ''').fetchall()
    conn.close()
    return render_template('index.html', pyqs=pyqs)

# Search page
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # Get data from the form
        department = request.form['department'].strip().upper()
        semester = request.form['semester'].strip()
        subject = request.form['subject'].strip().upper()
        exam = request.form['exam'].strip().lower()
        year = request.form['year'].strip()

        # Add checks for input
        errors = []
        if not validate_department_subject(department):
            errors.append("Invalid department name.")
        if not validate_semester(semester):
            errors.append("Semester must be an integer between 1 and 8.")
        if not validate_department_subject(subject):
            errors.append("Invalid subject name.")
        if not validate_exam(exam):
            errors.append("Exam must be either 'endsem' or 'midsem'.")
        if not validate_year(year):
            errors.append("Year must be between 2000 and 2100.")

        if errors:
            return render_template('index.html', errors=errors)

        conn = get_db_connection()
        # Render the results
        results = conn.execute('''SELECT * FROM pyqs WHERE 
                               department LIKE ? AND semester = ? 
                               AND subject LIKE ? AND exam = ? AND year = ? AND verified = 0 ''', 
                               (department, semester, f"%{subject}%", exam, year)).fetchall()
        
        verified_results = conn.execute('''SELECT * FROM pyqs WHERE 
                               department LIKE ? AND semester = ? 
                               AND subject LIKE ? AND exam = ? AND year = ? AND verified = 1 ''', 
                               (department, semester, f"%{subject}%", exam, year)).fetchall()
        conn.close()
        return render_template('results.html', results=results, verified_results=verified_results)
    # In case if GET
    return render_template('search.html')

# Download route for the carousel download button
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        errors = []
        # Check for captcha
        recaptcha_response = request.form.get('g-recaptcha-response', '')
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {'secret': RECAPTCHA_SECRET, 'response': recaptcha_response}
        r = requests.post(verify_url, data=payload)
        result = r.json()
        if not result.get('success'):
            errors.append("reCAPTCHA failed. Please try again.")

        # Check file and type of it
        if 'file' not in request.files:
            errors.append("No file part in the request")
        file = request.files['file']
        if file.filename == '':
            errors.append("No selected file")
        if not allowed_file(file.filename):
            errors.append("Invalid file type. Only .pdf are allowed.")
        
        # Check for file size
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        if file_length > MAX_CONTENT_LENGTH:
            errors.append("File is too large. Max allowed size is 5 MB.")

        # Get data from the form
        department = request.form['department'].strip().upper()
        semester = request.form['semester'].strip()
        subject = request.form['subject'].strip().upper()
        exam = request.form['exam'].strip().lower()
        year = request.form['year'].strip()

        # For unique naming to avoid collision
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Add chceks for input
        if not validate_department_subject(department):
            errors.append("Invalid department name.")
        if not validate_semester(semester):
            errors.append("Semester must be an integer between 1 and 8.")
        if not validate_department_subject(subject):
            errors.append("Invalid subject name.")
        if not validate_exam(exam):
            errors.append("Exam must be either 'End-Semester or 'Mid-Semester'.")
        if not validate_year(year):
            errors.append("Year must be between 2000 and 2100.")

        if errors:
            return render_template('upload.html', errors=errors)

        filename = secure_filename(f"{department}_{semester}_{subject}_{exam}_{year}_{timestamp}.pdf")

        conn = get_db_connection()
        # Check for duplicate files if already verified
        cursor = conn.execute('SELECT verified FROM pyqs WHERE filename = ?', (filename,))
        row = cursor.fetchone()
        if row and row['verified']:
            flash("Thank You for your contribution. Verified file already exists")
            conn.close()
            return redirect('/')

        # Save the file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn.execute(''' INSERT INTO pyqs(department, semester, subject, exam, year, filename)
                     VALUES(?, ?, ?, ?, ?, ?) ''', (department, semester, subject, exam, year, filename))
        conn.commit()
        conn.close()
        flash("File uploaded successfully")
        return redirect('/')
    # In case of GET
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
