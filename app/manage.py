from flask import Flask,url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import subqueryload
from app.utli import DateConverter
import datetime as dt


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
app.url_map.converters['date'] = DateConverter


def registerModuled():
    from app.subapps.admin.routing import adminRoute
    from app.subapps.home.routing import homeRoute
    from app.subapps.restfulAPI.routing import restRoute
    DEFAULT_MODULES = (
        (homeRoute, ''),
        (adminRoute, '/admin'),
        (restRoute, '/_restapi')
    )
    for module,url_prefix in DEFAULT_MODULES:
        app.register_blueprint(module, url_prefix=url_prefix)

    app.config['today'] = dt.date.today()
    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    from app.db_info import Session
    session = Session()
    user = session.query(User).options(subqueryload(User.address)).filter(User.id == user_id).first()
    session.close()
    return user