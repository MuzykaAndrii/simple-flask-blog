from flask import render_template, url_for, redirect, request, flash
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post
from app import bcrypt
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name = 'Software engeneering', title = 'PNU')

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
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # save data to database
        user = User(username, email, pw_hash)
        user.save()


        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
            
    return render_template('login.html', form=form, title='Login')

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user = {'nickname' : 'Andry'}
    posts = [
        {
            'author' : {'nickname' : 'Lohn'},
            'body' : "Beautifull day in Portland"
        },
        {
            'author' : {'nickname' : 'Susan'},
            'body' : "The Avengers movie was so cool"
        }
    ]
    return render_template('posts.html', title='Home', user=user, posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')