from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.admin_user import AdminUser
from app.models.db import db
from werkzeug.security import check_password_hash

admin_auth = Blueprint('admin_auth', __name__, url_prefix='/admin')

@admin_auth.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_auth.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'error')
            return render_template('admin/login.html')
        
        admin_user = AdminUser.query.filter_by(username=username).first()
        
        if admin_user and admin_user.check_password(password):
            login_user(admin_user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin_auth.admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@admin_auth.route('/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('admin_auth.admin_login'))

@admin_auth.route('/')
@admin_auth.route('/dashboard')
@login_required
def admin_dashboard():
    # Get some basic statistics for the dashboard
    from app.models.students import Student
    from app.models.courses import Course
    from app.models.sections import Section
    from app.models.faculties import Faculty
    
    stats = {
        'total_students': Student.query.count(),
        'total_courses': Course.query.count(),
        'total_sections': Section.query.count(),
        'total_faculty': Faculty.query.count(),
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin_auth.route('/create-admin', methods=['GET', 'POST'])
def create_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('admin/create_admin.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('admin/create_admin.html')
        
        if AdminUser.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('admin/create_admin.html')
        
        if AdminUser.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('admin/create_admin.html')
        
        admin_user = AdminUser(username=username, email=email)
        admin_user.set_password(password)
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            flash('Admin user created successfully!', 'success')
            return redirect(url_for('admin_auth.admin_login'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating admin user', 'error')
    
    return render_template('admin/create_admin.html') 