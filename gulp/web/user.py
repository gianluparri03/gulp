from flask import render_template, request, session, redirect
from functools import wraps

from gulp.web import app
from gulp.database import Users, GULPError
from gulp.database.users import User


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # Redirects anonymous users to the login page
        try:
            user = Users.get(session['user'])
            return func(user, *args, **kwargs)
        except (KeyError, GULPError):
            return redirect('/login')

    return inner


@app.route('/')
@login_required
def index(user):
    return render_template('index.html', name=user.name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Returns the form if it's a get request
    if request.method == 'GET':
        return render_template('login.html')

    # Fetches the request data
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    # Tries to execute the login
    try:
        user = Users.login(email, password)
        session['user'] = user.id
        return redirect('/')
    except GULPError as e:
        return render_template('login.html', error=str(e), email=email), 400

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Returns the form if it's a get request
    if request.method == 'GET':
        return render_template('signup.html')

    # Fetches the request data
    name = request.form.get('name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    # Tries to execute the signup
    try:
        user = Users.create(name, email, password)
        session['user'] = user.id
        return redirect('/')
    except GULPError as e:
        return render_template('signup.html', error=str(e), name=name, email=email), 400
