from flask import Blueprint, render_template, session, redirect, url_for, flash

supervisor = Blueprint('supervisor', __name__, url_prefix='/supervisor')

@supervisor.route('/dashboard')
def supervisor_dashboard():
    if not session.get('user') or session['user']['role'] != 'supervisor':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('supervisor/dashboard.html')

@supervisor.route('/workers')
def manage_workers():
    if not session.get('user') or session['user']['role'] != 'supervisor':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('supervisor/workers.html')

@supervisor.route('/tasks')
def manage_tasks():
    if not session.get('user') or session['user']['role'] != 'supervisor':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('supervisor/tasks.html') 