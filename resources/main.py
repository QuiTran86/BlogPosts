from flask import Blueprint, abort, flash, redirect, render_template, url_for, request, current_app
from flask_login import current_user, login_required

from assets.forms.password import PasswordResetForm
from assets.forms.posts import PostForm
from assets.forms.update_info import EditProfileForm, EditProfileAdminForm
from domain.permission import Permission
from infrastructure.models.posts import Post
from infrastructure.models.users import User
from infrastructure.models.roles import Role
from utils.decorators import admin_required, moderator_required

main = Blueprint('main', 'main')


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if current_user.can_do(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        post.save()
        flash('Post is created successfully!')
        return redirect(url_for('.index'))
    page_ind = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.published_at.desc()).paginate(page_ind, error_out=False,
                                                                        per_page=current_app.config[
                                                                            'FLASKY_POST_PER_PAGES'])
    posts = pagination.items
    return render_template('index.html', form=form, pagination=pagination, posts=posts)


@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    return 'hello'


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


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


@main.route('/update-prodile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def update_profile_for_admin(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.bio = form.bio.data
        user.save()
        flash(f'Updated profile for user: {user.username} successfully.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role
    form.name.data = user.name
    form.location.data = user.location
    form.bio.data = user.bio
    return render_template('edit_profile.html', form=form, user=user)


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
