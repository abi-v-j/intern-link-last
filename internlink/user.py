from internlink import app, db
from flask import redirect, render_template, request, session, url_for, flash
from flask_bcrypt import Bcrypt
import re
import os
from werkzeug.utils import secure_filename

flask_bcrypt = Bcrypt(app)
DEFAULT_USER_ROLE = 'student'

# File upload configuration
UPLOAD_FOLDER = 'internlink/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename, file_type='image'):
    if file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
    elif file_type == 'pdf':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
    return False

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

def user_home_url():
    """Generates a URL to the homepage for the currently logged-in user."""
    if 'loggedin' in session:
        role = session.get('role', None)
        if role == 'student':
            home_endpoint = 'student_home'
        elif role == 'employer':
            home_endpoint = 'employer_home'
        elif role == 'admin':
            home_endpoint = 'admin_home'
        else:
            home_endpoint = 'logout'
    else:
        home_endpoint = 'home'
    return url_for(home_endpoint)

@app.route('/')
def home():
    """Public homepage endpoint."""
    if 'loggedin' in session:
        return redirect(user_home_url())
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint."""
    if 'loggedin' in session:
        return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id, username, password_hash, role, status, full_name FROM users WHERE username = %s', (username,))
            account = cursor.fetchone()
            
            if account and flask_bcrypt.check_password_hash(account['password_hash'], password):
                if account['status'] == 'inactive':
                    flash('Your account has been deactivated. Please contact an administrator.', 'error')
                    return render_template('login.html', username=username)
                
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']
                session['status'] = account['status']
                session['full_name'] = account['full_name']
                return redirect(user_home_url())
            else:
                return render_template('login.html', username=username, username_invalid=not account, password_invalid=account)
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page endpoint for students."""
    if 'loggedin' in session:
        return redirect(user_home_url())
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        full_name = request.form['full_name']
        university = request.form['university']
        course = request.form['course']
        
        username_error = None
        email_error = None
        password_error = None
        confirm_password_error = None
        full_name_error = None
        university_error = None
        course_error = None
        
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                username_error = 'An account already exists with this username.'
            cursor.execute('SELECT user_id FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                email_error = 'An account already exists with this email address.'
            if len(username) > 20:
                username_error = 'Your username cannot exceed 20 characters.'
            if not re.match(r'^[A-Za-z0-9_]+$', username):
                username_error = 'Your username can only contain letters, numbers, and underscores.'
            if len(email) > 320:
                email_error = 'Your email address cannot exceed 320 characters.'
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                email_error = 'Invalid email address.'
            if len(password) < 8:
                password_error = 'Password must be at least 8 characters long.'
            if not re.search(r'[A-Z]', password):
                password_error = 'Password must contain at least one uppercase letter.'
            elif not re.search(r'[a-z]', password):
                password_error = 'Password must contain at least one lowercase letter.'
            elif not re.search(r'[0-9]', password):
                password_error = 'Password must contain at least one number.'
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                password_error = 'Password must contain at least one special character.'
            if password != confirm_password:
                confirm_password_error = 'Passwords do not match.'
            if not full_name or len(full_name.strip()) == 0:
                full_name_error = 'Full name is required.'
            if not university or len(university.strip()) == 0:
                university_error = 'University is required.'
            if not course or len(course.strip()) == 0:
                course_error = 'Course is required.'
            
            if any([username_error, email_error, password_error, confirm_password_error, 
                   full_name_error, university_error, course_error]):
                return render_template('signup.html', 
                                     username=username, email=email, full_name=full_name,
                                     university=university, course=course,
                                     username_error=username_error, email_error=email_error, 
                                     password_error=password_error, confirm_password_error=confirm_password_error,
                                     full_name_error=full_name_error, university_error=university_error,
                                     course_error=course_error)
            
            profile_image = 'default-avatar.png'
            resume_filename = None
            
            if 'profile_image' in request.files:
                file = request.files['profile_image']
                if file and file.filename != '' and allowed_file(file.filename, 'image'):
                    filename = secure_filename(f"{username}_profile_{file.filename}")
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    profile_image = filename
            
            if 'resume' in request.files:
                file = request.files['resume']
                if file and file.filename != '' and allowed_file(file.filename, 'pdf'):
                    filename = secure_filename(f"{username}_resume_{file.filename}")
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    resume_filename = filename
            
            password_hash = flask_bcrypt.generate_password_hash(password)
            cursor.execute('''INSERT INTO users (username, password_hash, email, full_name, role, status, 
                             university, course, profile_image, resume_filename) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                          (username, password_hash, email, full_name, DEFAULT_USER_ROLE, 'active',
                           university, course, profile_image, resume_filename))
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/profile')
@login_required()
def profile():
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT username, email, full_name, role, status, profile_image, 
                         university, course, resume_filename, company_name, company_description, 
                         company_website, company_logo FROM users WHERE user_id = %s''', (session['user_id'],))
        profile = cursor.fetchone()
    return render_template('profile.html', profile=profile)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required()
def edit_profile():
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT username, email, full_name, role, status, profile_image, 
                         university, course, resume_filename, company_name, company_description, 
                         company_website, company_logo FROM users WHERE user_id = %s''', (session['user_id'],))
        profile = cursor.fetchone()
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        
        if session['role'] == 'student':
            university = request.form['university']
            course = request.form['course']
            
            with db.get_cursor() as cursor:
                cursor.execute('''UPDATE users SET full_name = %s, email = %s, university = %s, course = %s 
                                 WHERE user_id = %s''', 
                              (full_name, email, university, course, session['user_id']))
        
        elif session['role'] == 'employer':
            company_name = request.form['company_name']
            company_description = request.form['company_description']
            company_website = request.form['company_website']
            
            with db.get_cursor() as cursor:
                cursor.execute('''UPDATE users SET full_name = %s, email = %s, company_name = %s, 
                                 company_description = %s, company_website = %s WHERE user_id = %s''', 
                              (full_name, email, company_name, company_description, company_website, session['user_id']))
        
        else:  # admin
            with db.get_cursor() as cursor:
                cursor.execute('UPDATE users SET full_name = %s, email = %s WHERE user_id = %s', 
                              (full_name, email, session['user_id']))
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', profile=profile)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required()
def change_password():
    """Change password endpoint."""
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s', (session['user_id'],))
            user = cursor.fetchone()
            
            if not flask_bcrypt.check_password_hash(user['password_hash'], current_password):
                flash('Current password is incorrect.', 'error')
                return render_template('change_password.html')
            
            if len(new_password) < 8:
                flash('New password must be at least 8 characters long.', 'error')
                return render_template('change_password.html')
            
            if not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or \
               not re.search(r'[0-9]', new_password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                flash('Password must contain uppercase, lowercase, number, and special character.', 'error')
                return render_template('change_password.html')
            
            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return render_template('change_password.html')
            
            if flask_bcrypt.check_password_hash(user['password_hash'], new_password):
                flash('New password cannot be the same as current password.', 'error')
                return render_template('change_password.html')
            
            new_password_hash = flask_bcrypt.generate_password_hash(new_password)
            cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s', 
                          (new_password_hash, session['user_id']))
            
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile'))
    
    return render_template('change_password.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('status', None)
    session.pop('full_name', None)
    return redirect(url_for('login'))
