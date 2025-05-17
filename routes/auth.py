from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from config.supabase_config import supabase
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        role = request.form.get('role', 'worker')  # Default role is worker
        
        # Check if user already exists
        try:
            existing_user = supabase.table('users').select('*').eq('email', email).execute()
            if existing_user.data:
                flash('Email already registered', 'error')
                return redirect(url_for('auth.register'))
            
            # Create new user
            new_user = {
                'uid': str(uuid.uuid4()),
                'email': email,
                'password_hash': generate_password_hash(password),
                'name': name,
                'role': role
            }
            
            result = supabase.table('users').insert(new_user).execute()
            
            if result.data:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Registration failed. Please try again.', 'error')
                
        except Exception as e:
            flash(f'Error during registration: {str(e)}', 'error')
            
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Get user by email
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            if result.data and len(result.data) > 0:
                user = result.data[0]
                if check_password_hash(user['password_hash'], password):
                    # Store user info in session
                    session['user'] = {
                        'id': user['id'],
                        'uid': user['uid'],
                        'email': user['email'],
                        'name': user['name'],
                        'role': user['role']
                    }
                    
                    # Redirect based on role
                    if user['role'] == 'admin':
                        return redirect(url_for('admin.admin_dashboard'))
                    elif user['role'] == 'supervisor':
                        return redirect(url_for('supervisor.supervisor_dashboard'))
                    elif user['role'] == 'worker':
                        return redirect(url_for('worker.worker_dashboard'))
                    elif user['role'] == 'client':
                        return redirect(url_for('client.client_dashboard'))
                else:
                    flash('Invalid password', 'error')
            else:
                flash('User not found', 'error')
                
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'error')
            
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


