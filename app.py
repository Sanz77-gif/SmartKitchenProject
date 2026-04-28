from flask import Flask, render_template, request, redirect, url_for
from database import db, init_db
from service import MealService
from models import Favorite

app = Flask(__name__)
init_db(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    query = request.form.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 5

    meals = MealService.search_meals(query) if query else []

    start = (page - 1) * per_page
    end = start + per_page
    meals_paginated = meals[start:end]

    page_fav = int(request.args.get('page_fav', 1))
    per_page_fav = 5

    favs_query = Favorite.query.order_by(Favorite.created_at.desc())

    favs = favs_query.offset((page_fav - 1) * per_page_fav).limit(per_page_fav).all()
    total_favs = favs_query.count()

    return render_template(
        'index.html',
        meals=meals_paginated,
        favs=favs,
        query=query,
        page=page,
        total=len(meals),

        page_fav=page_fav,
        total_favs=total_favs
    )

@app.route('/recipe/<meal_id>')
def recipe_detail(meal_id):
    meal = MealService.get_meal_by_id(meal_id)
    if not meal:
        return redirect(url_for('index'))

    return render_template('recipe.html', meal=meal, ingredients=[])

@app.route('/save', methods=['POST'])
def save():
    MealService.add_to_favorites({
        'id': request.form['id'],
        'name': request.form['name'],
        'img': request.form['img'],
        'cat': request.form['cat']
    })
    return redirect(url_for('index'))

@app.route('/delete/<meal_id>', methods=['POST'])
def delete(meal_id):
    MealService.delete_favorite(meal_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)