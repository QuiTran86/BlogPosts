from flask import Blueprint, flash, redirect, url_for, render_template, request, session
from flask_login import login_user, current_user, login_required, logout_user
from assets.forms.users import RegisterForm, LoginForm
from infrastructure.models.users import User
from notifications.email import send_email
from domain.permission import Permission

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


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirm(token):
        flash('Your confirmation successfully. Please try to login')
    else:
        flash('Your confirmation is invalid or token was expired')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_request = request.args.get('next')
            if next_request and next_request.startswith('/'):
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

@auth.route('/reset-password')
def reset_password():
    pass


