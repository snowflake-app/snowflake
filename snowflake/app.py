import json

from flask import Flask, url_for
from flask_login import LoginManager

from . import filters, settings
from .controllers import api, login, register, profile, index, one_on_one, appreciation, logout
from .models import User

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.login"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


app.register_blueprint(index.blueprint)
app.register_blueprint(api.users.blueprint, url_prefix="/api/users")
app.register_blueprint(login.blueprint, url_prefix="/login")
app.register_blueprint(register.blueprint, url_prefix="/register")
app.register_blueprint(profile.blueprint, url_prefix="/profile")
app.register_blueprint(one_on_one.blueprint, url_prefix="/1-on-1s")
app.register_blueprint(appreciation.blueprint)
app.register_blueprint(logout.blueprint, url_prefix="/logout")

app.add_template_filter(filters.humanize_time)
app.add_template_filter(filters.iso_time)
app.add_template_filter(filters.add_mentions)


@app.context_processor
def setup():
    def entrypoint(file: str):
        with open(app.static_folder + "/assets/manifest.json") as f:
            manifest = json.load(f)
            chunk = manifest[file]

            if app.debug:
                return 'http://localhost:8080/' + chunk
            else:
                return url_for('static', filename='assets/' + chunk)

    return {
        'entrypoint': entrypoint
    }
