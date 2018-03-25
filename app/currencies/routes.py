__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.currencies import bp
from app.currencies.forms import CurrencyForm, EditCurrencyForm
from app.models import Currency, Permission
from app.decorators import admin_required


@bp.route('/add_currency', methods=['GET', 'POST'])
@login_required
def add_currency():
    form = CurrencyForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        currency = Currency(name=form.name.data,
                            default=form.default.data,
                            user_id=current_user.id)
        db.session.add(currency)
        db.session.commit()
        flash('Currency has been created', 'success')
        return redirect(url_for('currencies.add_currency'))
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.desc()).paginate(page, 5, False)
    currencies = pagination.items
    return render_template('settings/add_currency.html', title='Add a Currency', form=form,
                           currencies=currencies, pagination=pagination)


@bp.route('/edit_currency/<id>', methods=['GET', 'POST'])
@login_required
def edit_currency(id):
    currency = Currency.query.filter_by(id=id).first()
    form = EditCurrencyForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        currency.name = form.name.data
        currency.default = form.default.data
        db.session.add(currency)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('currencies.add_currency'))
    elif request.method == 'GET':
        form.name.data = currency.name
        form.default.data = currency.default
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.desc()).paginate(page, 5, False)
    currencies = pagination.items
    return render_template('settings/edit_currency.html', title='Edit Currency', form=form,
                           currencies=currencies, pagination=pagination)


@bp.route('/delete_currency/<id>', methods=['POST'])
@login_required
@admin_required
def delete_currency(id):
    currency = Currency.query.get_or_404(id)
    db.session.delete(currency)
    db.session.commit()
    flash('Currency has been deleted successfully.', 'success')
    return redirect(url_for('currencies.edit_currency'))


@bp.route('/list_of_currencies')
@login_required
def list_of_currencies():
    page = request.args.get('page', 1, type=int)
    pagination = Currency.query.order_by(Currency.name.desc()).paginate(page, 5, False)
    currencies = pagination.items
    return render_template('settings/list_of_currencies.html', title='List of Currencies',
                           currencies=currencies, pagination=pagination)
