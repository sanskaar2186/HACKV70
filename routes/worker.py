from flask import Blueprint, render_template, session, redirect, url_for, flash

worker = Blueprint('worker', __name__, url_prefix='/worker')

@worker.route('/dashboard')
def worker_dashboard():
    if not session.get('user') or session['user']['role'] != 'worker':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('worker/dashboard.html')

@worker.route('/tasks')
def my_tasks():
    if not session.get('user') or session['user']['role'] != 'worker':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('worker/tasks.html')

@worker.route('/profile')
def profile():
    if not session.get('user') or session['user']['role'] != 'worker':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('worker/profile.html') 