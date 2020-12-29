from flask import Flask, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['markup'] = Markup
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login = LoginManager(app)
login.login_view = 'login'
login.sesion_protection = 'strong'
login.login_message_category = 'info'

ckeditor = CKEditor(app)

from app.posts.blueprint import posts
app.register_blueprint(posts, url_prefix='/blog')

from app.auth.blueprint import auth
app.register_blueprint(auth, url_prefix='/auth')

from app.api.blueprint import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

from app import views
from app.models import *

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
    form_overrides = dict(content=CKEditorField)
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'

    def is_accessible(self):
        return current_user.is_admin()


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(PostModelView(Post, db.session))
admin.add_view(UserModelView(User, db.session))

