import logging
from logging.handlers import SMTPHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app_var = Flask(__name__)
app_var.config.from_object(Config)
db = SQLAlchemy(app_var)
migrate = Migrate(app_var, db)
login = LoginManager(app_var)
login.login_view = 'login'


from app import routes, models, errors


if not app_var.debug:
    if app_var.config["MAIL_SERVER"]:
        auth = None
        if app_var.config['MAIL_USERNAME'] or app_var.config['MAIL_PASSWORD']:
            auth = (app_var.config['MAIL_USERNAME'],
                    app_var.config['MAIL_PASSWORD'])
        secure = None
        if app_var.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app_var.config['MAIL_SERVER'],
                      app_var.config['MAIL_PORT']),
            fromaddr='no-reply@'+app_var.config['MAIL_SERVER'],
            toaddrs=app_var.config['ADMINS'], subject='Noumenal Blog Error Log',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app_var.logger.addHandler(mail_handler)
