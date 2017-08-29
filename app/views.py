from flask import render_template
from run import app


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/Sign Up')
def sign_up():

    return render_template('Sign Up.html')


@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')