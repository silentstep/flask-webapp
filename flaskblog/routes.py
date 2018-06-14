from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt


posts = [
    {
        'author': 'Ventsi Nurkov',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'June 10, 2018',
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog post 2',
        'content': 'Second blog post',
        'date_posted': 'June 11, 2018',
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsucessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#@app.route("/account")
#def account():
#    return "<h1>Account page</h1>"