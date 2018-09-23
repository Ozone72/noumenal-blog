from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app_var, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from datetime import datetime


@app_var.route('/')
@app_var.route('/index')
@login_required
def index():
    user = {'username': 'Coach Pie'}
    posts = [
        {
            'author': {'username': 'Orin'},
            'body': 'A Crisp fall day in Seattle'
        },
        {
            'author': {'username': 'Vincent'},
            'body': 'Another day at werk...'
        },
        {
            'author': {'username': 'Josh'},
            'body': 'Money for nothing and my chicks for free :)'
        },
        {
            'author': {'username': 'Jed'},
            'body': 'MY band'
        },
        {
            'author': {'username': 'Brett'},
            'body': 'I love whiskey!'
        }

    ]
    return render_template('index.html', title='Home', posts=posts)


@app_var.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app_var.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you have been registered as a user!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app_var.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# this decorator includes a <dynamic component>
@app_var.route('/user/<username>')
@login_required
def user(username):  # the dynamic component is passed into this function
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


# adds a date time for last time this user was seen
@app_var.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app_var.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title="Edit Profile",
                           form=form)
