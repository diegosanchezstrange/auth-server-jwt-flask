import os
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)


app_settings = os.getenv('APP_SETTINGS', 'src.server.config.DevelopmentConfig')

app.config.from_object(app_settings)

#Just for development on localhost
app.config['MYSQL_USER']='diego'
app.config['MYSQL_PASSWORD']='p@ssword'
app.config['MYSQL_DB']='test'
app.config['MYSQL_HOST']='localhost'

#Creating the database instance
db = MySQL(app)

from .login import views
app.register_blueprint(views.bp)
