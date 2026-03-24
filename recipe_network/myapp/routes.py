from flask import render_template, redirect, url_for
from .models import Recipe, User, check_password_hash
from .forms import RecipeForm, RegistrationForm, LoginForm
from . import app, db
from flask_login import current_user, login_user, logout_user

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes = recipes)

@app.route('/new_recipe', methods = ['GET', 'POST'])
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(title = form.title.data, description = form.description.data)
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_recipe.html', title = "New Recipe", form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember = True)
            return redirect(url_for('home'))
        error = "Invalid Username or Password"
        return render_template('login.html', form = form, error = error)
    return render_template('login.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
        