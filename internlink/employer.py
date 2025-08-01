from internlink import app, db
from flask import redirect, render_template, session, url_for, request, flash
from datetime import datetime

def login_required(role=None):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'loggedin' not in session:
                return redirect(url_for('login'))
            if 'status' in session and session['status'] == 'inactive':
                flash('Your account has been Suspended. Please contact an admin.', 'error')
                return redirect(url_for('logout'))
            if role and session['role'] != role:
                return render_template('access_denied.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/employer/home')
@login_required(role='employer')
def employer_home():
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM internships WHERE employer_id = %s ORDER BY created_at DESC', (session['user_id'],))
        internships = cursor.fetchall()
        
        cursor.execute('''SELECT COUNT(*) as total_applications FROM applications a 
                         JOIN internships i ON a.internship_id = i.internship_id 
                         WHERE i.employer_id = %s''', (session['user_id'],))
        total_applications = cursor.fetchone()['total_applications']
        
        cursor.execute('''SELECT COUNT(*) as pending_applications FROM applications a 
                         JOIN internships i ON a.internship_id = i.internship_id 
                         WHERE i.employer_id = %s AND a.status = 'pending' ''', (session['user_id'],))
        pending_applications = cursor.fetchone()['pending_applications']
    
    return render_template('employer_home.html', 
                         internships=internships,
                         total_applications=total_applications,
                         pending_applications=pending_applications)

@app.route('/employer/internships')
@login_required(role='employer')
def employer_internships():
    with db.get_cursor() as cursor:
        cursor.execute('SELECT * FROM internships WHERE employer_id = %s ORDER BY created_at DESC', (session['user_id'],))
        internships = cursor.fetchall()
    return render_template('employer_internships.html', internships=internships)

@app.route('/employer/post', methods=['GET', 'POST'])
@login_required(role='employer')
def employer_post():
    """Post new internship endpoint."""
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        duration = request.form['duration']
        category = request.form['category']
        application_deadline = request.form['application_deadline']
        status = request.form['status']

        if len(title) > 100:
            return render_template('employer_post.html', error='Title must be 100 characters or less.')

        if status not in ['open', 'closed']:
            status = 'open'

        try:
            deadline_date = datetime.strptime(application_deadline, "%Y-%m-%d").date()
            if deadline_date < datetime.today().date():
                return render_template('employer_post.html', error='Application deadline must be a future date.')
        except ValueError:
            return render_template('employer_post.html', error='Invalid date format for application deadline.')

        with db.get_cursor() as cursor:
            cursor.execute('SELECT company_name FROM users WHERE user_id = %s', (session['user_id'],))
            employer = cursor.fetchone()
            company_name = employer['company_name'] if employer else ''

            cursor.execute('''
                INSERT INTO internships (
                    employer_id, title, description, company_name,
                    location, application_deadline, duration,
                    category, created_at, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
            ''', (
                session['user_id'], title, description, company_name,
                location, application_deadline, duration,
                category, status
            ))

        flash('Internship posted successfully!', 'success')
        return redirect(url_for('employer_home'))

    return render_template('employer_post.html')


@app.route('/employer/applications')
@login_required(role='employer')
def employer_applications():
    search_name = request.args.get('search_name', '')
    search_title = request.args.get('search_title', '')
    search_status = request.args.get('search_status', '')
    
    with db.get_cursor() as cursor:
        query = '''SELECT a.*, i.title, u.full_name as student_name, u.email as student_email,
                   u.university, u.course FROM applications a 
                   JOIN internships i ON a.internship_id = i.internship_id 
                   JOIN users u ON a.student_id = u.user_id 
                   WHERE i.employer_id = %s'''
        params = [session['user_id']]
        
        if search_name:
            query += ' AND u.full_name LIKE %s'
            params.append(f'%{search_name}%')
        if search_title:
            query += ' AND i.title LIKE %s'
            params.append(f'%{search_title}%')
        if search_status:
            query += ' AND a.status = %s'
            params.append(search_status)
        
        query += ' ORDER BY a.submission_date DESC'
        cursor.execute(query, params)
        applications = cursor.fetchall()
    
    return render_template('employer_applications.html', 
                         applications=applications,
                         search_name=search_name,
                         search_title=search_title,
                         search_status=search_status)

@app.route('/employer/update_application/<int:application_id>/<status>', methods=['GET', 'POST'])
@login_required(role='employer')
def employer_update_application(application_id, status):
    if status not in ['accepted', 'rejected']:
        return render_template('access_denied.html'), 403
    
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT i.employer_id, a.*, i.title, u.full_name as student_name 
                         FROM applications a 
                         JOIN internships i ON a.internship_id = i.internship_id 
                         JOIN users u ON a.student_id = u.user_id
                         WHERE a.application_id = %s''', (application_id,))
        result = cursor.fetchone()
        
        if not result or result['employer_id'] != session['user_id']:
            return render_template('access_denied.html'), 403
        
        if request.method == 'POST':
            reason = request.form.get('reason', '')
            cursor.execute('UPDATE applications SET status = %s, reason = %s WHERE application_id = %s', 
                          (status, reason, application_id))
            flash(f'Application {status} successfully!', 'success')
            return redirect(url_for('employer_applications'))
    
    return render_template('employer_update_application.html', 
                         application=result, 
                         new_status=status)
