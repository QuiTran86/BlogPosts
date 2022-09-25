from flask import Blueprint, flash, redirect, url_for, render_template

from assets.forms.users import RegisterForm
from infrastructure.models.users import User
from notifications.email import send_email

auth = Blueprint('auth', 'auth')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        user.save()
        token = user.generate_confirmed_token()
        send_email('New User Confirmation', 'assets/templates/mail/confirm',
                   to='tranvy2017@gmail.com', user=user, token=token)
        flash('A confirmation email has been sent to you. It will be expired in 5 mins. '
              'Please check your email!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, current_user=None)



