from flask import render_template, flash,redirect, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db

from . import bp 
from app.forms import RegisterForm, SigninForm

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not email and not user:
            u = User(username=username, email=form.email.data)
            u.password = u.hash_password(form.password.data)
            u.add_token()
            u.commit()
            flash(f'{username} registered', 'success')
            return redirect(url_for("main.home"))
        if user:
            flash(f'{username} already taken, try again!', 'warning')
        elif email:
            flash(f'{form.email.data} has already taken, try again!', 'warning')
    return render_template('register.jinja', title="Matrix Fakebook: Register Page", form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    signin_form = SigninForm() 
    if signin_form.validate_on_submit():
        user = User.query.filter_by(username=signin_form.username.data).first()
        if user and user.check_password(signin_form.password.data):
            flash(f'{signin_form.username.data} signed in', 'success')
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash(f'{signin_form.username.data} doesn\'t exist or incorrect password', 'warning')
    return render_template('signin.jinja', title='Sign In Page', form=signin_form)
