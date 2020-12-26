from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login = LoginManager(app)
login.login_view = 'login'
login.sesion_protection = 'strong'
login.login_message_category = 'info'

from app import views
from app.models import *

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_admin()

admin = Admin(app)
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(User, db.session))

