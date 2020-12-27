from flask import Blueprint, render_template, request, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app.models import User
from app import bcrypt
from flask_login import current_user, login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/')
def redirect_auth():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

####### LOGIN
@auth.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
        else:
            flash(f'{result.username}, you have been logged in!', category='success')
            login_user(result, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('index'))
            
    return render_template('auth/login.html', form=form, title='Login')

######### LOGOUT
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))