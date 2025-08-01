from internlink import app, db
from flask import redirect, render_template, session, url_for, request, flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

flask_bcrypt = Bcrypt(app)


UPLOAD_FOLDER = 'internlink/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  

def allowed_file(filename, file_type='image'):
    if file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
    elif file_type == 'pdf':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

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

@app.route('/admin/home')
@login_required(role='admin')
def admin_home():
    with db.get_cursor() as cursor:
        cursor.execute('SELECT COUNT(*) AS user_count FROM users')
        user_count = cursor.fetchone()['user_count']
        cursor.execute('SELECT COUNT(*) AS internship_count FROM internships')
        internship_count = cursor.fetchone()['internship_count']
        cursor.execute('SELECT COUNT(*) AS application_count FROM applications')
        application_count = cursor.fetchone()['application_count']
        cursor.execute('SELECT COUNT(*) AS active_users FROM users WHERE status = "active"')
        active_users = cursor.fetchone()['active_users']
    
    return render_template('admin_home.html', 
                         user_count=user_count, 
                         internship_count=internship_count, 
                         application_count=application_count,
                         active_users=active_users)

@app.route('/admin/users')
@login_required(role='admin')
def admin_users():
    search_name = request.args.get('search_name', '')
    search_role = request.args.get('search_role', '')
    search_status = request.args.get('search_status', '')
    
    with db.get_cursor() as cursor:
        query = 'SELECT user_id, username, email, full_name, role, status FROM users WHERE 1=1'
        params = []
        
        if search_name:
            query += ' AND full_name LIKE %s'
            params.append(f'%{search_name}%')
        if search_role:
            query += ' AND role = %s'
            params.append(search_role)
        if search_status:
            query += ' AND status = %s'
            params.append(search_status)
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        users = cursor.fetchall()
    
    return render_template('admin_users.html', 
                         users=users,
                         search_name=search_name,
                         search_role=search_role,
                         search_status=search_status)

@app.route('/admin/user/<int:user_id>')
@login_required(role='admin')
def admin_view_user(user_id):
    with db.get_cursor() as cursor:
        cursor.execute('''SELECT * FROM users WHERE user_id = %s''', (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
    
    return render_template('admin_view_user.html', user=user)

@app.route('/admin/toggle_user_status/<int:user_id>')
@login_required(role='admin')
def admin_toggle_user_status(user_id):
    if user_id == session['user_id']:
        flash('Cannot change your own account status.', 'error')
        return redirect(url_for('admin_users'))
    
    with db.get_cursor() as cursor:
        cursor.execute('SELECT status FROM users WHERE user_id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
        
        new_status = 'inactive' if user['status'] == 'active' else 'active'
        cursor.execute('UPDATE users SET status = %s WHERE user_id = %s', (new_status, user_id))
        flash(f'User status changed to {new_status}.', 'success')
    
    return redirect(url_for('admin_users'))
@app.route('/admin/create_user', methods=['GET', 'POST'])
@login_required(role='admin')
def admin_create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        role = request.form['role']
        image_file = request.files.get('profile_image')

        username_error = None
        password_error = None

        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                username_error = 'Username already exists.'
            elif len(username) > 20 or not username.replace('_', '').isalnum():
                username_error = 'Username must be alphanumeric and up to 20 characters.'

            if len(password) < 8:
                password_error = 'Password must be at least 8 characters.'

            if username_error or password_error:
                return render_template('admin_create_user.html', username=username, email=email,
                                       full_name=full_name, role=role,
                                       username_error=username_error,
                                       password_error=password_error)

            if role not in ['employer', 'admin']:
                role = 'employer'

            profile_image = 'default-avatar.png'
            if image_file and image_file.filename != '' and allowed_file(image_file.filename, 'image'):
                filename = secure_filename(f"{username}_profile_{image_file.filename}")
                upload_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(upload_path)
                profile_image = filename

            password_hash = flask_bcrypt.generate_password_hash(password)

            cursor.execute('''
                INSERT INTO users (username, password_hash, email, full_name, role, status, profile_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (username, password_hash, email, full_name, role, 'active', profile_image))

        flash('User created successfully!', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin_create_user.html')
