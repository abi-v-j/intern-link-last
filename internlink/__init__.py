from flask import Flask
import os

app = Flask(__name__)
app.secret_key = 'internlink_secret_key_1234567890abcdef'

UPLOAD_FOLDER = 'internlink/static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

from internlink import connect
from internlink import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname, connect.dbport)

from internlink import user
from internlink import student
from internlink import employer
from internlink import admin
