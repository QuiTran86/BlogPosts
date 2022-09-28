from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_user
from assets.forms.users import RegisterForm, LoginForm
from infrastructure.models.users import User
from notifications.email import send_email
from urllib.parse import urlparse, urljoin

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
def confirm(token):
    return f'{token}'


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


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    pass
