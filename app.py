from flask import Flask, render_template, request, redirect, url_for, Blueprint

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

from routes.auth import auth

app.register_blueprint(auth)


if __name__ == '__main__':
    app.run(debug=True)