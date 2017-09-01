from flask import render_template, session, redirect, url_for, flash, request
from functools import wraps
from run import app


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html')


@app.route('/Sign Up', methods=['GET', 'POST'])
def sign_up():

    return render_template('Sign Up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Username or Password.'
        else:
            session['logged_in'] = True
            flash('You have now been logged in!')
            return redirect(url_for('dashboard'))
    return render_template('index.html', error=error)


@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out!')
        return redirect(url_for('login'))