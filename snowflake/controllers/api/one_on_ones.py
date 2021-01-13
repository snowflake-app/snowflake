from datetime import datetime

from flask import Blueprint, request
from flask_login import login_required, current_user
from marshmallow import ValidationError

from .response import not_found, unauthorized, no_content, bad_request, validation_error
from ... import acl
from ...db import transaction, db
from ...models import OneOnOne, OneOnOneActionItem
from ...schemas.one_on_one import OneOnOneSchema, GetOneOnOneSchema, CreateOneOnOneSchema, OneOnOneActionItemSchema, \
    CreateOrEditOneOnOneActionItemSchema

blueprint = Blueprint('api.one_on_ones', __name__)

one_on_one_schema = OneOnOneSchema()
one_on_one_action_item_schema = OneOnOneActionItemSchema()
get_one_on_one_schema = GetOneOnOneSchema()
create_one_on_one_schema = CreateOneOnOneSchema()
create_or_edit_one_on_one_action_item_schema = CreateOrEditOneOnOneActionItemSchema()


@login_required
@blueprint.route('', methods=['GET'])
def list_all_one_on_one():
    return one_on_one_schema.jsonify(OneOnOne.get_by_user(current_user), many=True)


@login_required
@blueprint.route('', methods=['PUT'])
def create_one_on_one():
    if not request.is_json:
        return bad_request()

    try:
        one_on_one: OneOnOne = create_one_on_one_schema.load(request.json)
        one_on_one.created_by = current_user
        one_on_one.created_at = datetime.now()

        with transaction():
            OneOnOne.create(one_on_one)

        return get_one_on_one_schema.jsonify(one_on_one)
    except ValidationError as e:
        return validation_error(e.messages)


@login_required
@blueprint.route('/<_id>', methods=['GET'])
def get_one_on_one(_id: int):
    one_on_one = OneOnOne.get(_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    return get_one_on_one_schema.jsonify(one_on_one)


@login_required
@blueprint.route('/<_id>', methods=['DELETE'])
def delete_one_on_one(_id: int):
    one_on_one = OneOnOne.get(_id)

    if not one_on_one:
        return not_found()

    if not acl.can_delete_one_on_one(one_on_one):
        return unauthorized()

    with transaction():
        db.session.remove(one_on_one)

    return no_content()


@login_required
@blueprint.route('/<one_on_one_id>/action_items', methods=['GET'])
def list_action_items(one_on_one_id: int):
    one_on_one = OneOnOne.get(one_on_one_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    return one_on_one_action_item_schema.jsonify(one_on_one.action_items, many=True)


@login_required
@blueprint.route('/<one_on_one_id>/action_items', methods=['PUT'])
def create_action_item(one_on_one_id: int):
    if not request.is_json:
        return bad_request()

    one_on_one = OneOnOne.get(one_on_one_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    try:
        action_item: OneOnOneActionItem = create_or_edit_one_on_one_action_item_schema.load(request.json)
        action_item.one_on_one = one_on_one
        action_item.created_by = current_user
        action_item.created_at = datetime.now()

        with transaction():
            OneOnOneActionItem.create(action_item)

        return one_on_one_action_item_schema.jsonify(action_item)
    except ValidationError as e:
        return validation_error(e.messages)


@login_required
@blueprint.route('/<one_on_one_id>/action_items/<action_item_id>', methods=['GET'])
def get_action_item(one_on_one_id: int, action_item_id: int):
    one_on_one = OneOnOne.get(one_on_one_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    action_item = OneOnOneActionItem.get(action_item_id)

    if not action_item:
        return not_found()

    if not action_item.one_on_one_id == one_on_one.id:
        return not_found()

    return one_on_one_action_item_schema.jsonify(action_item)


@login_required
@blueprint.route('/<one_on_one_id>/action_items/<action_item_id>', methods=['PATCH'])
def edit_action_item(one_on_one_id: int, action_item_id: int):
    if not request.is_json:
        return bad_request()

    one_on_one = OneOnOne.get(one_on_one_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    action_item = OneOnOneActionItem.get(action_item_id)

    try:
        action_item: OneOnOneActionItem = create_or_edit_one_on_one_action_item_schema.load(request.json, action_item)

        with transaction():
            db.session.add(action_item)

        return one_on_one_action_item_schema.jsonify(action_item)
    except ValidationError as e:
        return validation_error(e.messages)


@login_required
@blueprint.route('/<one_on_one_id>/action_items/<action_item_id>', methods=['DELETE'])
def delete_action_item(one_on_one_id: int, action_item_id: int):
    one_on_one = OneOnOne.get(one_on_one_id)

    if not one_on_one:
        return not_found()

    if not acl.can_view_one_on_one(one_on_one):
        return unauthorized()

    action_item = OneOnOneActionItem.get(action_item_id)

    if not action_item:
        return not_found()

    if not action_item.one_on_one_id == one_on_one.id:
        return not_found()

    with transaction():
        db.session.remove(one_on_one)

    return no_content()
