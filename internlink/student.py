from internlink import app, db
from flask import redirect, render_template, session, url_for, request, flash
from datetime import datetime
import os
from werkzeug.utils import secure_filename

def login_required(role=None):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session:
                return redirect(url_for('login'))
            if 'status' in session and session['status'] == 'inactive':
                flash('Your account has been deactivated. Please contact an administrator.', 'error')
                return redirect(url_for('logout'))
            if role and session['role'] != role:
                return render_template('access_denied.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@app.route('/student/home')
@login_required(role='student')
def student_home():
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')
    duration_filter = request.args.get('duration', '')
    
    with db.get_cursor() as cursor:
        query = "SELECT * FROM internships WHERE status = 'open'"
        params = []
        
        if category_filter:
            query += " AND category = %s"
            params.append(category_filter)
        if location_filter:
            query += " AND location LIKE %s"
            params.append(f"%{location_filter}%")
        if duration_filter:
            query += " AND duration = %s"
            params.append(duration_filter)
        
        query += " ORDER BY created_at DESC LIMIT 5"
        cursor.execute(query, params)
        internships = cursor.fetchall()
        
        cursor.execute('''SELECT a.*, i.title, i.company_name FROM applications a 
                         JOIN internships i ON a.internship_id = i.internship_id 
                         WHERE a.student_id = %s ORDER BY a.submission_date DESC LIMIT 5''', 
                      (session['user_id'],))
        applications = cursor.fetchall()
        
        cursor.execute("SELECT DISTINCT category FROM internships WHERE status = 'open' ORDER BY category")
        categories = [row['category'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT location FROM internships WHERE status = 'open' ORDER BY location")
        locations = [row['location'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT duration FROM internships WHERE status = 'open' ORDER BY duration")
        durations = [row['duration'] for row in cursor.fetchall()]
    
    return render_template('student_home.html', 
                         internships=internships, 
                         applications=applications,
                         categories=categories,
                         locations=locations,
                         durations=durations,
                         current_category=category_filter,
                         current_location=location_filter,
                         current_duration=duration_filter)

@app.route('/student/internships')
@login_required(role='student')
def student_internships():
    category_filter = request.args.get('category', '')
    location_filter = request.args.get('location', '')
    duration_filter = request.args.get('duration', '')
    
    with db.get_cursor() as cursor:
        query = "SELECT * FROM internships WHERE status = 'open'"
        params = []
        
        if category_filter:
            query += " AND category = %s"
            params.append(category_filter)
        if location_filter:
            query += " AND location LIKE %s"
            params.append(f"%{location_filter}%")
        if duration_filter:
            query += " AND duration = %s"
            params.append(duration_filter)
        
        query += " ORDER BY application_deadline ASC"
        cursor.execute(query, params)
        internships = cursor.fetchall()
        
        cursor.execute("SELECT DISTINCT category FROM internships WHERE status = 'open' ORDER BY category")
        categories = [row['category'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT location FROM internships WHERE status = 'open' ORDER BY location")
        locations = [row['location'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT duration FROM internships WHERE status = 'open' ORDER BY duration")
        durations = [row['duration'] for row in cursor.fetchall()]
    
    return render_template('student_internships.html', 
                         internships=internships,
                         categories=categories,
                         locations=locations,
                         durations=durations,
                         current_category=category_filter,
                         current_location=location_filter,
                         current_duration=duration_filter)

@app.route('/student/apply/<int:internship_id>', methods=['GET', 'POST'])
@login_required(role='student')
def student_apply(internship_id):
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM internships WHERE internship_id = %s', (internship_id,))
        internship = cursor.fetchone()
        if not internship or internship['status'] != 'open':
            flash('This internship is not available for applications.', 'error')
            return redirect(url_for('student_internships'))
        
        cursor.execute('''SELECT full_name, email, university, course, resume_filename 
                         FROM users WHERE user_id = %s''', (session['user_id'],))
        student = cursor.fetchone()
        
        if request.method == 'POST':
            cursor.execute('SELECT * FROM applications WHERE student_id = %s AND internship_id = %s', 
                          (session['user_id'], internship_id))
            if cursor.fetchone():
                flash('You have already applied for this internship.', 'error')
                return render_template('student_apply.html', internship=internship, student=student)
            
            cover_letter = request.form['cover_letter']
            resume_filename = student['resume_filename']
            
            if 'resume' in request.files:
                file = request.files['resume']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(f"{session['username']}_resume_{file.filename}")
                    file.save(os.path.join('internlink/static/uploads', filename))
                    resume_filename = filename
                    
                    cursor.execute('UPDATE users SET resume_filename = %s WHERE user_id = %s', 
                                  (resume_filename, session['user_id']))
            
            cursor.execute('''INSERT INTO applications (student_id, internship_id, status, submission_date, 
                             cover_letter, resume_filename) VALUES (%s, %s, %s, %s, %s, %s)''',
                          (session['user_id'], internship_id, 'pending', datetime.now(), 
                           cover_letter, resume_filename))
            
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('student_applications'))
    
    return render_template('student_apply.html', internship=internship, student=student)

@app.route('/student/applications')
@login_required(role='student')
def student_applications():
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT a.*, i.title, i.company_name, i.location, i.duration 
                         FROM applications a JOIN internships i ON a.internship_id = i.internship_id 
                         WHERE a.student_id = %s ORDER BY a.submission_date DESC''', 
                      (session['user_id'],))
        applications = cursor.fetchall()
    return render_template('student_applications.html', applications=applications)
