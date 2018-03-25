__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.category_types import bp
from app.category_types.forms import CategoryTypeForm, EditCategoryTypeForm
from app.models import CategoryType, Permission
from app.decorators import admin_required


@bp.route('/add_category_type', methods=['GET', 'POST'])
@login_required
def add_category_type():
    form = CategoryTypeForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        category_type = CategoryType(name=form.name.data,
                                     icon=form.icon.data,
                                     user_id=current_user.id)
        db.session.add(category_type)
        db.session.commit()
        flash('Category Type has been created', 'success')
        return redirect(url_for('category_types.add_category_type'))
    page = request.args.get('page', 1, type=int)
    pagination = CategoryType.query.order_by(CategoryType.name.desc()).paginate(page, 5, False)
    category_types = pagination.items
    return render_template('settings/add_category_type.html', title='Add a Category Type', form=form,
                           category_types=category_types, pagination=pagination)


@bp.route('/edit_category_type/<id>', methods=['GET', 'POST'])
@login_required
def edit_category_type(id):
    category_type = CategoryType.query.filter_by(id=id).first()
    form = EditCategoryTypeForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        category_type.name = form.name.data
        category_type.icon = form.icon.data
        db.session.add(category_type)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('category_types.add_category_type'))
    elif request.method == 'GET':
        form.name.data = category_type.name
        form.icon.data = category_type.icon
    page = request.args.get('page', 1, type=int)
    pagination = CategoryType.query.order_by(CategoryType.name.desc()).paginate(page, 5, False)
    category_types = pagination.items
    return render_template('settings/edit_category_type.html', title='Edit Category Type', form=form,
                           category_types=category_types, pagination=pagination)


@bp.route('/delete_category_type/<id>', methods=['POST'])
@login_required
@admin_required
def delete_category_type(id):
    category_type = CategoryType.query.get_or_404(id)
    db.session.delete(category_type)
    db.session.commit()
    flash('Category Type has been deleted successfully.', 'success')
    return redirect(url_for('category_types.edit_category_type'))


@bp.route('/list_of_category_types')
@login_required
def list_of_category_types():
    page = request.args.get('page', 1, type=int)
    pagination = CategoryType.query.order_by(CategoryType.name.desc()).paginate(page, 5, False)
    category_types = pagination.items
    return render_template('settings/list_of_category_types.html', title='List of category types',
                           category__types=category_types, pagination=pagination)
