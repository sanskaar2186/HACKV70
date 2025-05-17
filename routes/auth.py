from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from firebase_admin import auth as firebase_auth
from config.firebase_config import firebase_app
from config.supabase_config import supabase
from models.user import User, UserRole
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Verify with Firebase
            user = firebase_auth.get_user_by_email(email)
            
            # Get user data from Supabase
            result = supabase.table('users').select('*').eq('uid', user.uid).execute()
            user_data = result.data[0] if result.data else None
            
            if not user_data:
                flash('User not found in database', 'error')
                return redirect(url_for('auth.login'))
            
            # Store user in session
            session['user'] = user_data
            
            # Redirect based on role
            if user_data['role'] == UserRole.ADMIN.value:
                return redirect(url_for('admin_dashboard'))
            elif user_data['role'] == UserRole.SUPERVISOR.value:
                return redirect(url_for('supervisor_dashboard'))
            elif user_data['role'] == UserRole.WORKER.value:
                return redirect(url_for('worker_dashboard'))
            else:
                return redirect(url_for('client_dashboard'))
                
        except Exception as e:
            flash('Invalid credentials', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            role = request.form.get('role', UserRole.CLIENT.value)

            if not all([email, password, name]):
                flash('All fields are required', 'error')
                return redirect(url_for('auth.register'))

            # Create user in Firebase
            try:
                user = firebase_auth.create_user(
                    email=email,
                    password=password,
                    display_name=name
                )
            except Exception as e:
                flash(f'Firebase error: {str(e)}', 'error')
                return redirect(url_for('auth.register'))
            
            # Create user data for Supabase
            user_data = {
                'uid': user.uid,
                'email': email,
                'name': name,
                'role': role,
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Store in Supabase
            try:
                result = supabase.table('users').insert(user_data).execute()
                if not result.data:
                    # If Supabase insert fails, delete the Firebase user
                    firebase_auth.delete_user(user.uid)
                    flash('Error storing user data', 'error')
                    return redirect(url_for('auth.register'))
            except Exception as e:
                # If Supabase insert fails, delete the Firebase user
                firebase_auth.delete_user(user.uid)
                flash(f'Supabase error: {str(e)}', 'error')
                return redirect(url_for('auth.register'))
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
                
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


