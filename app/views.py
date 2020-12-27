from flask import render_template, url_for, redirect, request, flash, abort
from app import app
from app.forms import UpdateAccountForm, UpdatePasswordForm, CreatePostForm
from app.models import User
from app import bcrypt
from flask_login import current_user, login_required
from . import db
from datetime import datetime as dt
import os
import secrets
from PIL import Image
from functools import wraps

@app.before_request
def update_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = dt.now()
        db.session.commit()

def save_picture(form_picture):
    #generate random name for pic
    random_hex = secrets.token_hex(8)

    #divide filename to name and extentions
    f_name, f_ext, = os.path.splitext(form_picture.filename)

    #connect new pic name to her extention
    picture_fn = random_hex + f_ext

    #generate new pic path according to new name and os folders position
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    #define default pic size
    output_size = (200, 200)

    #open, crop and save pic
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name = 'Software engeneering', title = 'PNU')


###################### ACCOUNT SETTINGS ##########################

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    pass_form = UpdatePasswordForm()

    if pass_form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, pass_form.old_password.data):
            current_user.password = bcrypt.generate_password_hash(pass_form.new_password.data).decode('utf-8')
            db.session.commit()
            flash('The password changed')
            return render_template('user/account.html', title='Account', image_file=image_file, form=form, pass_form=pass_form)
        else:
            flash('Wrong old password')  

    #for pressed update button
    if form.validate_on_submit():

        #if added new account image
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        #update user data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        #save all database changes
        db.session.commit()

        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    #for page loaded
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me
    
    #loading page
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user/account.html', title='Account', image_file=image_file, form=form, pass_form=pass_form)
