from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



login_manager = LoginManager()
login_manager.login_view="homeRoute.login"


#create app and config app
config_file='config.py'

# def create_app(config_file='config.py'):

app = Flask(__name__)
app.config.from_pyfile(config_file, silent=False)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager.init_app(app)


def registerModuled():
    from app.subapps.admin.routing import adminRoute
    from app.subapps.home.routing import homeRoute
    DEFAULT_MODULES = (
        (homeRoute, ''),
        (adminRoute, '/admin')
    )
    for module,url_prefix in DEFAULT_MODULES:
        app.register_blueprint(module, url_prefix=url_prefix)
    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.filter_by(id=user_id).first()