from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required
from domain.permission import Permission
from infrastructure import db
from infrastructure.models.posts import Post
from assets.forms.posts import PostForm

from assets.forms.password import PasswordResetForm

main = Blueprint('main', 'main')


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if current_user.can_do(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data)
        post.save()
        flash('Post is created successfully!')
        return redirect(url_for('.index'))
    return render_template('index.html', form=form)


@main.route('/update-password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        current_user.password = form.password2.data
        current_user.save()
        flash('Your password is updated successfully!')
        return redirect(url_for('main.index'))
    return render_template('updated_info.html')


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)