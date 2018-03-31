__author__ = 'Cedric Da Costa Faro'

from sqlalchemy import func
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
from flask_login import current_user, login_required
from app import db
from app.expenses import bp
from app.expenses.forms import ExpenseForm, EditExpenseForm, ListExpenseForm
from app.models import Expense, Permission, Client, Project, CategoryType
from app.decorators import admin_required


@bp.route('/_get_projects')
def _get_projects():
    client_id = request.args.get('client_id', '01', type=str)
    projects_id = [(row.id, row.name) for row in Project.query.filter_by(client_id=client_id).all()]
    return jsonify(projects_id)


@bp.route('/_get_categories')
def _get_categories():
    category_id = request.args.get('category_id', '01', type=str)
    category_types_id = [(row.id, row.name) for row in CategoryType.query.filter_by(category_id=category_id).all()]
    return jsonify(category_types_id)


@bp.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm(form_name='PickExpense')
    form.client_id.choices = [(row.id, row.name) for row in Client.query.all()]
    form.project_id.choices = [(row.id, row.name) for row in Project.query.all()]
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = current_user.my_expenses().paginate(page, 4, False)
        expenses = pagination.items
        return render_template('expenses/add_expense.html', title='Add an expense', form=form, expenses=expenses,
                               pagination=pagination)
    if current_user.can(Permission.WRITE) and form.validate_on_submit() and request.form['form_name'] == 'PickExpense':
        expense = Expense(date=form.date.data,
                          name=form.name.data,
                          location=form.location.data,
                          category_id=form.category_id.data.id,
                          category_type_id=form.category_type_id.data.id,
                          amount=form.amount.data,
                          currency_id=form.currency_id.data.id,
                          guest=form.guest.data,
                          guest_list=form.guest_list.data,
                          client_id=form.client_id.data.id,
                          project_id=form.project_id.data.id,
                          user_expense=current_user)
        db.session.add(expense)
        db.session.commit()
        flash('Your Expense has been added!', 'success')
        return redirect(url_for('expenses.add_expense'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.my_expenses().paginate(page, 4, False)
    expenses = pagination.items
    return render_template('expenses/add_expense.html', title='Add an expense', form=form, expenses=expenses,
                           pagination=pagination)


@bp.route('/edit_expense/<id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    form = EditExpenseForm(form_name='PickExpense')
    form.client_id.choices = [(row.id, row.name) for row in Client.query.all()]
    form.project_id.choices = [(row.id, row.name) for row in Project.query.all()]
    if current_user.can(Permission.WRITE) and form.validate_on_submit() and request.form['form_name'] == 'PickExpense':
        expense.date = form.date.data
        expense.name = form.name.data
        expense.location = form.location.data
        expense.category_id = form.category_id.data.id
        expense.category_type_id = form.category_type_id.data.id
        expense.amount = form.amount.data
        expense.currency_id = form.currency_id.data.id
        expense.guest = form.guest.data
        expense.guest_list = form.guest_list.data
        expense.client_id = form.client_id.data.id
        expense.project_id = form.project_id.data.id
        db.session.add(expense)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('expenses.edit_expense', id=id))
    elif request.method == 'GET':
        form.date.data = expense.date
        form.name.data = expense.name
        form.location.data = expense.location
        form.category_id.data = expense.category_expense
        form.category_type_id.data = expense.category_type_expense
        form.amount.data = expense.amount
        form.currency_id.data = expense.currency_expense
        form.guest.data = expense.guest
        form.guest_list.data = expense.guest_list
        form.client_id.data = expense.client_expense
        form.project_id.data = expense.project_expense
    page = request.args.get('page', 1, type=int)
    pagination = current_user.my_expenses().paginate(page, 4, False)
    expenses = pagination.items
    return render_template('expenses/edit_expense.html', title='Edit Expense', form=form, expenses=expenses,
                           pagination=pagination, id=id)


@bp.route('/delete_expense/<id>', methods=['POST'])
@login_required
@admin_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense has been deleted successfully.', 'success')
    return redirect(url_for('expenses.add_expense'))


@bp.route('/my_expenses', methods=['GET', 'POST'])
@login_required
def my_expenses():
    expense_search = current_user.my_expenses()
    form = ListExpenseForm()
    if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        expense_search = expense_search.filter(func.date(Expense.date) >= date_from,
                                               func.date(Expense.date) <= date_to)
    page = request.args.get('page', 1, type=int)
    pagination = expense_search.paginate(page, current_app.config['TASKS_PER_PAGE'], False)
    expenses = pagination.items
    return render_template('expenses/my_expenses.html', title='My Expenses', expenses=expenses, pagination=pagination,
                           form=form)


@bp.route('/list_of_expenses', methods=['GET', 'POST'])
@login_required
def list_of_expenses():
    expense_search = Expense.query
    form = ListExpenseForm()
    if form.validate_on_submit():
        date_from = form.date_from.data
        date_to = form.date_to.data
        category = form.category_id.data
        category_type = form.category_type_id.data
        client = form.client_id.data
        project = form.project_id.data
        expense_search = expense_search.filter(func.date(Expense.date) >= date_from,
                                               func.date(Expense.date) <= date_to,
                                               Expense.category_id == category.id,
                                               Expense.category_type_id == category_type.id,
                                               Expense.client_id == client.id,
                                               Expense.project_id == project.id)
    page = request.args.get('page', 1, type=int)
    pagination = expense_search.paginate(page, current_app.config['TASKS_PER_PAGE'], False)
    expenses = pagination.items
    return render_template('expenses/list_of_expenses.html', title='List of Expenses', expenses=expenses,
                           pagination=pagination, form=form)
