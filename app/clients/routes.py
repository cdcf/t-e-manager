__author__ = 'Cedric Da Costa Faro'

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.clients import bp
from app.clients.forms import ClientForm, EditClientForm
from app.models import Client, Permission
from app.decorators import admin_required


@bp.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    form = ClientForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        client = Client(name=form.name.data,
                        address=form.address.data,
                        user_id=current_user.id)
        db.session.add(client)
        db.session.commit()
        flash('Client account has been created', 'success')
        return redirect(url_for('clients.add_client'))
    page = request.args.get('page', 1, type=int)
    pagination = Client.query.order_by(Client.name.desc()).paginate(page, 5, False)
    clients = pagination.items
    return render_template('clients/add_client.html', title='Add a Client Account', form=form, clients=clients,
                           pagination=pagination)


@bp.route('/edit_client/<id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.filter_by(id=id).first()
    form = EditClientForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        client.name = form.name.data
        client.address = form.address.data
        db.session.add(client)
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('clients.edit_client', id=id))
    elif request.method == 'GET':
        form.name.data = client.name
        form.address.data = client.address
    page = request.args.get('page', 1, type=int)
    pagination = Client.query.order_by(Client.name.desc()).paginate(page, 5, False)
    clients = pagination.items
    return render_template('clients/edit_client.html', title='Edit a Client', form=form, clients=clients,
                           pagination=pagination, id=id)


@bp.route('/delete_client/<id>', methods=['POST'])
@login_required
@admin_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Client has been deleted successfully.', 'success')
    return redirect(url_for('clients.add_client'))


@bp.route('/list_of_clients')
@login_required
def list_of_clients():
    page = request.args.get('page', 1, type=int)
    pagination = Client.query.order_by(Client.name.desc()).paginate(page, 5, False)
    clients = pagination.items
    return render_template('clients/list_of_clients.html', title='List of clients', clients=clients,
                           pagination=pagination)
