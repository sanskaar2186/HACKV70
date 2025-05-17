from flask import Blueprint, render_template, session, redirect, url_for, flash

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
def admin_dashboard():
    if not session.get('user') or session['user']['role'] != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')

@admin.route('/users')
def manage_users():
    if not session.get('user') or session['user']['role'] != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('admin/users.html')

@admin.route('/services')
def manage_services():
    if not session.get('user') or session['user']['role'] != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('admin/services.html')