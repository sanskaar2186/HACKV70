from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash, session
from config.firebase_config import firebase_app
from config.supabase_config import supabase
from datetime import datetime
from routes.auth import auth
from routes.admin import admin
from routes.supervisor import supervisor
from routes.worker import worker
from routes.client import client
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

Secret_key = ' ljvnlbuibejlvbdjbdgdjdd'
app.config['SECRET_KEY'] = Secret_key

# Initialize Fire

@app.route('/')
def index():
    return render_template('index.html')

# Import and register blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(supervisor)
app.register_blueprint(worker)
app.register_blueprint(client)

# Add datetime filter
@app.template_filter('datetime')
def format_datetime(value):
    if not value:
        return ''
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value.strftime('%Y-%m-%d %H:%M:%S')

@app.template_filter('date')
def format_date(value):
    if not value:
        return ''
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value.strftime('%Y-%m-%d')

@app.template_filter('time')
def format_time(value):
    if not value:
        return ''
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return value.strftime('%H:%M:%S')

# Custom filters
@app.template_filter('status_color')
def status_color(status):
    colors = {
        'pending': 'warning',
        'in_progress': 'primary',
        'completed': 'success',
        'delayed': 'danger'
    }
    return colors.get(status, 'secondary')

@app.template_filter('priority_color')
def priority_color(priority):
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger'
    }
    return colors.get(priority, 'secondary')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

if __name__ == '__main__':
    app.run(debug=True)