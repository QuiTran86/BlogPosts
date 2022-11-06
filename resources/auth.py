from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from assets.forms.password import PasswordResetForm, PasswordUpdateForm
from assets.forms.users import LoginForm, RegisterForm
from infrastructure.models.users import User
from notifications.email import send_email
from services.users import UserService

auth = Blueprint('auth', 'auth')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        user.save()
        token = user.generate_confirmed_token()
        send_email('New User Confirmation', 'mail/confirm.txt',
                   to='tranvy2017@gmail.com', user=user, token=token)
        flash('A confirmation email has been sent to you. It will be expired in 5 mins. '
              'Please check your email!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<email>/<token>')
def confirm(email, token):
    user = UserService().find_user_by_email(email=email)
    if user.confirm(token):
        flash('Your confirmation successfully. Please try to login')
    else:
        flash('Your confirmation is invalid or token was expired')
    return redirect(url_for('auth.login'))


@auth.route('/confirm-reset-password/<email>/<token>')
def confirm_reset_password(email, token):
    user = UserService().find_user_by_email(email=email)
    if user.confirm(token):
        flash('Your confirmation is successful')
        return redirect(url_for('.update_password', email=user.email))
    else:
        flash('Your confirmation is invalid or token was expired')
    return redirect(url_for('.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_request = request.args.get('next')
            if next_request is None or (next_request and next_request.startswith('/')):
                next_request = url_for('main.index')
            return redirect(next_request)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logout successfully!')
    return redirect(url_for('.login'))


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = UserService().find_user_by_email(email=form.email.data)
        user.mark_as_forgot_password()
        token = user.generate_confirmed_token()
        send_email('Update New Password Confirmation', 'mail/confirm_reset_password.txt',
                   to='tranvy2017@gmail.com', user=user, token=token)
        flash('A confirmation email has been sent to you. It will be expired in 5 mins. '
              'Please check your email!')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth.route('/update-password/<email>', methods=['GET', 'POST'])
def update_password(email):
    user = UserService().find_user_by_email(email)
    form = PasswordUpdateForm()
    if form.validate_on_submit():
        user.password = form.password2.data
        user.save()
        flash('Your password is updated successfully!')
        return redirect(url_for('auth.login'))
    return render_template('updated_password.html', form=form)
