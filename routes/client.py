from flask import Blueprint, render_template, session, redirect, url_for, flash

client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/dashboard')
def client_dashboard():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/dashboard.html')

@client.route('/services')
def my_services():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/services.html')

@client.route('/profile')
def profile():
    if not session.get('user') or session['user']['role'] != 'client':
        flash('Access denied', 'error')
        return redirect(url_for('auth.login'))
    return render_template('client/profile.html') 