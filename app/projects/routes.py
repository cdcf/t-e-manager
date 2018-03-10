__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.projects import bp
from app.projects.forms import ProjectForm, EditProjectForm
from app.models import Project, Permission
from app.decorators import admin_required


@bp.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data,
                          description=form.description.data,
                          user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash('Project has been created', 'success')
        return redirect(url_for('projects.add_project'))
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.name.desc()).paginate(page, 5, False)
    projects = pagination.items
    return render_template('projects/add_project.html', title='Add a Project', form=form, projects=projects,
                           pagination=pagination)


@bp.route('/edit_project/<id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.filter_by(id=id).first()
    form = EditProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        db.session.add(project)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('projects.add_project'))
    elif request.method == 'GET':
        form.name.data = project.name
        form.description.data = project.description
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.name.desc()).paginate(page, 5, False)
    projects = pagination.items
    return render_template('projects/edit_project.html', title='Edit Project', form=form, projects=projects,
                           pagination=pagination)


@bp.route('/delete_project/<id>', methods=['POST'])
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted successfully.', 'success')
    return redirect(url_for('projects.add_project'))


@bp.route('/list_of_projects')
@login_required
def list_of_projects():
    page = request.args.get('page', 1, type=int)
    pagination = Project.query.order_by(Project.name.desc()).paginate(page, 5, False)
    projects = pagination.items
    return render_template('projects/list_of_projects.html', title='List of projects', projects=projects,
                           pagination=pagination)
