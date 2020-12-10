from flask import Blueprint, request, session, redirect, url_for, render_template
from flask_login import login_user

from snowflake.forms import RegistrationForm
from snowflake.models import User

blueprint = Blueprint('register', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        unique_id = session['unique_id']
        users_email = session['users_email']
        picture = session['picture']
        full_name = session['users_name']
        username = users_email.split("@")[0]

        user = User(id_=unique_id, email=users_email, name=full_name, profile_pic=picture,
                    team_name=form.team_name.data, designation=form.designation.data, username=username)

        User.create(user)

        login_user(user)

        return redirect(url_for('index.index'))

    return render_template('welcome.html', form=form, user_name=session['users_name'], picture=session['picture'])
