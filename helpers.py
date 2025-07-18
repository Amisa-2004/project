import re

ALLOWED_EXTENSIONS = {'pdf'}
VALID_EXAM_TYPES = {'endsem', 'midsem'}

# Check for .pdf files
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Check for valid semester
def validate_semester(semester_str):
    if not semester_str.isdigit():
        return False
    sem = int(semester_str)
    return 1 <= sem <= 8

# Check for a valid year
def validate_year(year_str):
    if not year_str.isdigit():
        return False
    yr = int(year_str)
    return 2000 <= yr <= 2100

# Check for valid exam types
def validate_exam(exam_str):
    return exam_str.lower() in VALID_EXAM_TYPES

# Check for valid subject
def validate_department_subject(value):
    return bool(re.match(r'^[A-Za-z0-9\s]+$', value))
