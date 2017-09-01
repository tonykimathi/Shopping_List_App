from flask import render_template, session, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from app.forms import RegisterForm, LoginForm
from app.models import User
from functools import wraps
from app import app


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

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        first_name = form.username.data
        last_name = form.username.data

        email = form.email.data
        password = generate_password_hash(form.password.data)

        if User.register(username, email, first_name, last_name, password) is True:
            user = User.current_user(email)
            session['logged_in'] = True
            session['username'] = username
            session['email'] = email
            session['password'] = password
            session['id'] = user['_id']
            flash('You have been registered!  {} '.format(username), 'success')
            print(session['id'])
            print(User.users)
            return redirect(url_for('dashboard'))
        else:
            flash('Email exists!!! You can login instead!', 'error')
            return redirect(url_for('login_user'))
    return render_template('Sign Up.html',
                           form=form
                           )


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """ The user login method"""
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        if User.user_exists(email) is True:
            if User.user_login_verify(email, password) is True:
                user = User.current_user(email)
                session['logged_in'] = True
                session['username'] = user['username']
                session['email'] = email
                session['password'] = user['password']
                session['id'] = user['_id']
                flash('You have successfully logged in!!', 'success')
                print(session['id'])
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid Login!! Password or Email incorrect', 'error')
                return redirect(url_for('login_user'))
        else:
            flash("Email do not exist!!  first register")
            return redirect(url_for('register_user'))
    return render_template('login.html',
                           form=form
                           )


@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out!')
        return redirect(url_for('login'))