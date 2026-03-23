from flask import render_template
from .models import Recipe
from . import app, db

@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('home.html', recipes = recipes)