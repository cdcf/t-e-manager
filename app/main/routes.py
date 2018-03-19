__author__ = 'Cedric Da Costa Faro'

from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EditProfileAdminForm
from app.models import User, Task, Role
from app.main import bp
from app.decorators import admin_required


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    tasks = user.tasks.order_by(Task.date.desc()).paginate(page, current_app.config['TASKS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=tasks.next_num) if tasks.has_next else None
    prev_url = url_for('main.user', username=user.username, page=tasks.prev_num) if tasks.has_prev else None
    return render_template('users/user.html', user=user, tasks=tasks.items, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/edit_profile/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user, original_username=user.username, original_email=user.email)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.about_me = form.about_me.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('main.user', username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.about_me.data = user.about_me
        form.role.data = Role.query.get(user.role_id)
    return render_template('users/edit_profile.html', title='Edit Profile', form=form, user=user)


@bp.route('/list_of_users')
@login_required
def list_of_users():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.username.asc()).paginate(page, 5, False)
    users = pagination.items
    return render_template('users/list_of_users.html', title='List of users', users=users,
                           pagination=pagination)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'danger')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!', 'danger')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following {}'.format(username), 'success')
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'danger')
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!', 'danger')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are no longer following {}'.format(username), 'success')
    return redirect(url_for('main.user', username=username))
