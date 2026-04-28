import requests
from database import db
from models import Favorite

class MealService:
    API_KEY = "340d84b85f3d4b66bbf9a8a5bfed163c"
    BASE_URL = "https://api.spoonacular.com/recipes/"

    @staticmethod
    def search_meals(query):
        try:
            url = f"{MealService.BASE_URL}complexSearch"
            params = {
                "query": query,
                "number": 10,
                "apiKey": MealService.API_KEY
            }

            response = requests.get(url, params=params)
            data = response.json()

            meals = data.get("results", [])

            return [{
                "idMeal": m["id"],
                "strMeal": m["title"],
                "strMealThumb": m["image"],
                "strCategory": "Food"
            } for m in meals]

        except Exception as e:
            print("Ошибка поиска:", e)
            return []

    @staticmethod
    def get_meal_by_id(meal_id):
        try:
            url = f"{MealService.BASE_URL}{meal_id}/information"
            params = {"apiKey": MealService.API_KEY}

            response = requests.get(url, params=params)
            data = response.json()

            return {
                "strMeal": data.get("title"),
                "strMealThumb": data.get("image"),
                "strCategory": "Food",
                "strArea": "Unknown",
                "strInstructions": data.get("instructions") or "Нет инструкции",
                "strYoutube": ""
            }

        except Exception as e:
            print("Ошибка рецепта:", e)
            return None

    @staticmethod
    def add_to_favorites(data):
        if not Favorite.query.get(data['id']):
            new_fav = Favorite(
                meal_id=data['id'],
                name=data['name'],
                image=data['img'],
                category=data.get('cat', 'Food')
            )
            db.session.add(new_fav)
            db.session.commit()

            if Favorite.query.count() > 20:
                oldest = Favorite.query.order_by(Favorite.created_at).first()
                db.session.delete(oldest)
                db.session.commit()

    @staticmethod
    def delete_favorite(meal_id):
        fav = Favorite.query.get(meal_id)
        if fav:
            db.session.delete(fav)
            db.session.commit()