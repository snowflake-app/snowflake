import json

from flask import Flask, url_for

from . import db, filters, settings, migrations, logger
from .controllers import api, login, register, profile, index, one_on_one, appreciation, logout, \
    notifications
from .marshmallow import marshmallow
from .redis import redis
from .services import login_manager
from .services.session_interface import CustomSessionInterface

logger.setup()


def create_app():
    app = Flask(__name__)

    settings.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    marshmallow.init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(api.healthcheck.blueprint, url_prefix="/api/healthcheck")
    app.register_blueprint(index.blueprint)

    app.register_blueprint(api.notifications.blueprint, url_prefix="/api/notifications")
    app.register_blueprint(api.one_on_ones.blueprint, url_prefix="/api/one_on_ones")
    app.register_blueprint(api.token.blueprint, url_prefix="/api/tokens")
    app.register_blueprint(api.users.blueprint, url_prefix="/api/users")

    app.register_blueprint(login.blueprint, url_prefix="/login")
    app.register_blueprint(register.blueprint, url_prefix="/register")
    app.register_blueprint(profile.blueprint, url_prefix="/profile")
    app.register_blueprint(one_on_one.blueprint, url_prefix="/1-on-1s")
    app.register_blueprint(appreciation.blueprint)
    app.register_blueprint(notifications.blueprint, url_prefix="/notifications")
    app.register_blueprint(logout.blueprint, url_prefix="/logout")

    app.add_template_filter(filters.humanize_time)
    app.add_template_filter(filters.iso_time)
    app.add_template_filter(filters.add_mentions)

    app.session_interface = CustomSessionInterface(key_prefix='session', redis=redis)

    @app.context_processor
    def setup():  # pragma: no cover, pylint: disable=unused-variable
        def entrypoint(file: str):
            with open(f"{app.static_folder}/assets/manifest.json") as manifest_file:
                manifest = json.load(manifest_file)
                chunk = manifest[file]

                if app.debug:
                    return 'http://localhost:8080/' + chunk

                return url_for('static', filename='assets/' + chunk)

        def choose_plural(size, singular, plural):
            return plural if size != 1 else singular

        return {
            'entrypoint': entrypoint,
            'choose_plural': choose_plural,
        }

    @app.cli.command('migrate')
    def migrate():  # pragma: no cover, pylint: disable=unused-variable
        migrations.migrate()

    return app
