# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/app/app.db' % BASE_DIR
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '\xff\x93\xc8w\x13\x0e3\xd6\x82\x0f\x84\x18\xe7\xd9\\|\x04e\xb9(\xfd\xc3'
ADMIN_USER = 'admin'
ADMIN_PASSWD = 'passw0rd'
DEFAULT_APP_NAME = 'AppointmentSys'
PORT = 5001
HOST = '127.0.0.1'



