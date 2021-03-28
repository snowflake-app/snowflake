from flask import Blueprint, url_for, redirect, render_template, flash
from flask_login import login_required, current_user

from snowflake import db
from snowflake.forms import OneOnOneForm, OneOnOneActionItemForm, OneOnOneActionItemStateChange
from snowflake.models import User, OneOnOne, OneOnOneActionItem
from snowflake.services import notification

blueprint = Blueprint('one_on_one', __name__)


@blueprint.route('/', methods=['POST', 'GET'], defaults={'_id': None})
@blueprint.route('/<_id>', methods=['POST', 'GET'])
@login_required
def one_on_one(_id):
    form = OneOnOneForm()
    action_item_form = OneOnOneActionItemForm()
    action_item_state_change_form = OneOnOneActionItemStateChange()

    if form.validate_on_submit():
        user = User.get_by_username(form.user.data)

        if user is not None:
            new_one_on_one = OneOnOne(user=user, created_by=current_user)

            with db.transaction():
                db.persist(new_one_on_one)
                notification.notify_one_on_one_setup(new_one_on_one)

            return redirect(url_for("one_on_one.one_on_one"))

        form.user.errors.append("User not found")
        flash(f'User {form.user.data} not found', category='warning')

    one_on_ones = OneOnOne.get_by_user(current_user)
    current_one_on_one = OneOnOne.get(_id) if _id is not None else one_on_ones[0] if len(
        one_on_ones) > 0 else None

    return render_template('1-on-1s.html',
                           one_on_ones=one_on_ones,
                           form=form,
                           action_item_form=action_item_form,
                           action_item_state_change_form=action_item_state_change_form,
                           one_on_one=current_one_on_one)


@blueprint.route('/action-items', methods=['POST'])
@login_required
def one_on_one_action_item():
    form = OneOnOneActionItemForm()

    if form.validate():
        new_one_on_one = OneOnOne.get(form.one_on_one.data)
        action_item = OneOnOneActionItem(content=form.content.data, one_on_one=new_one_on_one,
                                         created_by=current_user, state=False)
        with db.transaction():
            db.persist(action_item)
            notification.notify_one_on_one_action_item_added(action_item)

    return redirect(f'/1-on-1s/{form.one_on_one.data}')


@blueprint.route('/action-items/done', methods=['POST'])
@login_required
def one_on_one_action_item_done():
    form = OneOnOneActionItemStateChange()
    if form.validate_on_submit():
        action_item_data = form.action_item.data
        action_item = OneOnOneActionItem.get(action_item_data)
        action_item.state = 1

        with db.transaction():
            db.persist(action_item)

        return redirect(f'/{action_item.one_on_one.id}')

    return url_for('one_on_one.one_on_one')
