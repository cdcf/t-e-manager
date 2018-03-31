__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.categories import bp
from app.categories.forms import CategoryForm, EditCategoryForm
from app.models import Category, Permission
from app.decorators import admin_required


@bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        category = Category(name=form.name.data,
                            colour=form.colour.data)
        db.session.add(category)
        db.session.commit()
        flash('Category has been created', 'success')
        return redirect(url_for('categories.add_category'))
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(Category.name.desc()).paginate(page, 5, False)
    categories = pagination.items
    return render_template('settings/add_category.html', title='Add a Category', form=form, categories=categories,
                           pagination=pagination)


@bp.route('/edit_category/<id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.filter_by(id=id).first()
    form = EditCategoryForm(category.name)
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        category.name = form.name.data
        category.colour = form.colour.data
        db.session.add(category)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('categories.edit_category', id=id))
    elif request.method == 'GET':
        form.name.data = category.name
        form.colour.data = category.colour
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(Category.name.desc()).paginate(page, 5, False)
    categories = pagination.items
    return render_template('settings/edit_category.html', title='Edit a Category', form=form, categories=categories,
                           pagination=pagination, id=id)


@bp.route('/delete_category/<id>', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted successfully.', 'success')
    return redirect(url_for('categories.add_category'))


@bp.route('/list_of_categories')
@login_required
def list_of_categories():
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(Category.name.desc()).paginate(page, 5, False)
    categories = pagination.items
    return render_template('settings/list_of_categories.html', title='List of categories', categories=categories,
                           pagination=pagination)
