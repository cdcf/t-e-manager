__author__ = 'Cedric Da Costa Faro'

from datetime import date
from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.tasks import bp
from app.tasks.forms import TaskForm, EditTaskForm, ListTaskForm
from app.models import Task, Permission, Client, Project
from app.decorators import admin_required


@bp.route('/_get_projects/')
def _get_projects():
    client_id = request.args.get('client_id', '01', type=str)
    projects_id = [(row.id, row.name) for row in Project.query.filter_by(client_id=client_id).all()]
    return jsonify(projects_id)


@bp.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm(form_name='PickTask')
    form.client_id.choices = [(row.id, row.name) for row in Client.query.all()]
    form.project_id.choices = [(row.id, row.name) for row in Project.query.all()]
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = current_user.my_tasks().filter(func.date(Task.date) == date.today()).order_by(Task.date.desc(),
                                                                                                   Task.jira.asc()).paginate(
            page, 4, False)
        tasks = pagination.items
        return render_template('tasks/add_task.html', title='Add a task', form=form, tasks=tasks, pagination=pagination)
    if current_user.can(Permission.WRITE) and form.validate_on_submit() and request.form['form_name'] == 'PickTask':
        task = Task(name=form.name.data,
                    client_id=form.client_id.data.id,
                    project_id=form.project_id.data.id,
                    user_task=current_user,
                    jira=form.jira.data,
                    duration=form.duration.data,
                    date=form.date.data,
                    rate=form.rate.data,
                    comment=form.comment.data)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been added!', 'success')
        return redirect(url_for('tasks.add_task'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.my_tasks().filter(func.date(Task.date) == date.today()).order_by(Task.date.desc(),
                                                                                          Task.jira.asc()).paginate(
        page, 4, False)
    tasks = pagination.items
    return render_template('tasks/add_task.html', title='Add a task', form=form, tasks=tasks, pagination=pagination)


@bp.route('/edit_task/<id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.filter_by(id=id).first()
    form = EditTaskForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        task.name = form.name.data
        task.client_id = form.client_id.data.id
        task.project_id = form.project_id.data.id
        task.jira = form.jira.data
        task.duration = form.duration.data
        task.date = form.date.data
        task.rate = form.rate.data
        task.comment = form.comment.data
        db.session.add(task)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('tasks.add_task'))
    elif request.method == 'GET':
        form.name.data = task.name
        form.client_id.data = task.client_task
        form.project_id.data = task.project_task
        form.jira.data = task.jira
        form.duration.data = task.duration
        form.date.data = task.date
        form.rate.data = task.rate
        form.comment.data = task.comment
    page = request.args.get('page', 1, type=int)
    pagination = current_user.my_tasks().paginate(page, 4, False)
    tasks = pagination.items
    return render_template('tasks/edit_task.html', title='Edit Task', form=form, tasks=tasks, pagination=pagination)


@bp.route('/delete_task/<id>', methods=['POST'])
@login_required
@admin_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted successfully.', 'success')
    return redirect(url_for('tasks.add_task'))


@bp.route('/my_tasks', methods=['GET', 'POST'])
@login_required
def my_tasks():
    task_search = current_user.my_tasks()
    form = ListTaskForm()
    if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        task_search = task_search.filter(func.date(Task.date) >= date_from, func.date(Task.date) <= date_to)
    page = request.args.get('page', 1, type=int)
    pagination = task_search.paginate(page, current_app.config['TASKS_PER_PAGE'], False)
    tasks = pagination.items
    return render_template('tasks/my_tasks.html', title='My Tasks', tasks=tasks, pagination=pagination, form=form)


@bp.route('/my_followed_tasks')
@login_required
def my_followed_tasks():
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followed_tasks().order_by(Task.date.desc(), Task.client_id.asc(), Task.jira.asc()).paginate(
        page, current_app.config['TASKS_PER_PAGE'], False)
    tasks = pagination.items
    return render_template('tasks/my_followed_tasks.html', title='My Followed Tasks', tasks=tasks, pagination=pagination)


@bp.route('/list_of_tasks')
@login_required
def list_of_tasks():
    page = request.args.get('page', 1, type=int)
    pagination = Task.query.order_by(Task.date.desc(), Task.client_id.asc(), Task.jira.asc()).paginate(
        page, current_app.config['TASKS_PER_PAGE'], False)
    tasks = pagination.items
    return render_template('tasks/list_of_tasks.html', title='List of tasks', tasks=tasks, pagination=pagination)
