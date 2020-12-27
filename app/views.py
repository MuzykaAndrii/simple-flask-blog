from flask import render_template, url_for, redirect, request, flash, abort
from app import app
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, UpdatePasswordForm, CreatePostForm
from app.models import User
from app import bcrypt
from flask_login import current_user, login_user, logout_user, login_required
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


######################## LOGIN AND REGISTER LOGIC ##########################
####### REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():

        # gather data from form
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # save data to database
        user = User(username, email, password)
        user.save()


        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('login'))
    return render_template('auth-reg/register.html', title='Register', form=form)

####### LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    #redirect if loggined
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():

        #gather data
        email = form.email.data
        password = form.password.data

        #check if user exist and password hash is equals
        result = User.query.filter_by(email=email).first()
        if result is None or not bcrypt.check_password_hash(result.password, password):
            flash('Login unsuccessfull. Please check username and password', category='warning')
            return redirect(url_for('login'))
        else:
            flash(f'{result.username}, you have been logged in!', category='success')
            login_user(result, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
            
    return render_template('auth-reg/login.html', form=form, title='Login')

######### LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

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
