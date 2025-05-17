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


if __name__ == '__main__':
    app.run(debug=True)