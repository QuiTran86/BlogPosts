from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from assets.forms.password import PasswordResetForm
from assets.forms.posts import PostForm
from assets.forms.update_info import EditProfileForm
from domain.permission import Permission
from infrastructure.models.posts import Post
from infrastructure.models.users import User
from utils.decorators import admin_required, moderator_required

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
    return render_template('updated_password.html', form=form)


@main.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        current_user.save()
        flash('Your profile has been updated successfully.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('edit_profile.html', form=form)


@main.route('/user/<username>')
def user(username):
    user_md = User.query.filter_by(username=username).first()
    if not user_md:
        abort(404)
    return render_template('user.html', user=user_md)


@main.route('/admin')
@login_required
@admin_required
def admin():
    return 'For admin only'


@main.route('/moderator')
@login_required
@moderator_required
def moderator():
    return 'For moderator only'


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
