from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from config.firebase_config import firebase_app
from config.supabase_config import supabase

app = Flask(__name__)

Secret_key = ' ljvnlbuibejlvbdjbdgdjdd'
app.config['SECRET_KEY'] = Secret_key

# Initialize Fire

@app.route('/')
def index():
    return render_template('index.html')

# Import and register blueprints
from routes.auth import auth
from routes.admin import admin
from routes.supervisor import supervisor
from routes.worker import worker
from routes.client import client

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(supervisor)
app.register_blueprint(worker)
app.register_blueprint(client)

# Dashboard routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('user') or session['user']['role'] != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

@app.route('/supervisor/dashboard')
def supervisor_dashboard():
    if not session.get('user') or session['user']['role'] != 'supervisor':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('supervisor/dashboard.html')

@app.route('/worker/dashboard')
def worker_dashboard():
    if not session.get('user') or session['user']['role'] != 'worker':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('worker/dashboard.html')

@app.route('/client/dashboard')
def client_dashboard():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)