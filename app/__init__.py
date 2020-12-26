from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
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

# class with identify admin method

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()


class UserModelView(ModelView):
    form_create_rules = ['username', 'email', 'password', 'about_me', 'admin']

    form_edit_rules  = ['username', 'email', 'about_me', 'admin']


    def on_model_change(self, form, model, is_created):
        model.hash_password(form.password.data)
        return super(BaseModelView, self).on_model_change(form, model, is_created)
    
    def is_accessible(self):
        return current_user.is_admin()

class PostModelView(ModelView):
    form_columns = ['title', 'content', 'author']

    def is_accessible(self):
        return current_user.is_admin()


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(PostModelView(Post, db.session))
admin.add_view(UserModelView(User, db.session))

