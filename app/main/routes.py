from flask import render_template, request, jsonify, current_app, send_from_directory
import os
from flask_login import current_user
from app.main import bp
from app.models import Recipe, Like
from app import db
from sqlalchemy import desc, func
from app.services.meal_api import MealDBAPI, ErrorCode

@bp.route('/')
@bp.route('/index')
def index():
    try:
        # Get random meals from API for inspiration if API key is available
        api_recipes = []
        if current_app.config.get('SPOONACULAR_API_KEY'):
            try:
                api_recipes = MealDBAPI.get_random_meals(6)
            except Exception as api_error:
                error_message = str(api_error)
                if hasattr(api_error, 'code'):
                    if api_error.code == ErrorCode.AuthenticationError:
                        current_app.logger.error("Invalid API key - disabling API features")
                        current_app.config['SPOONACULAR_API_KEY'] = None
                    elif api_error.code == ErrorCode.QuotaExceeded:
                        current_app.logger.warning("Daily API quota exceeded")
                current_app.logger.error(f"Error fetching API recipes: {error_message}")
        
        # Get recent user-submitted recipes, including those with 0 likes
        try:
            user_recipes = db.session.query(Recipe, func.count(Like.id).label('like_count'))\
                .outerjoin(Like)\
                .group_by(Recipe.id)\
                .order_by(desc('like_count'), desc(Recipe.created_at))\
                .limit(6)\
                .all()
        except Exception as db_error:
            current_app.logger.error(f"Error fetching user recipes: {str(db_error)}")
            user_recipes = []
        
        # Convert to list of Recipe objects
        user_recipes = [recipe for recipe, _ in user_recipes]
        
        return render_template('main/index.html', 
                             title='CookTheLefts - Finde Rezepte mit deinen Zutaten',
                             api_recipes=api_recipes,
                             user_recipes=user_recipes)
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        return render_template('main/index.html', 
                             title='CookTheLefts - Finde Rezepte mit deinen Zutaten',
                             api_recipes=[],
                             user_recipes=[])

@bp.route('/search')
def search():
    try:
        # Get and clean ingredients from query parameters
        ingredients_param = request.args.get('ingredients', '')
        if not ingredients_param:
            return jsonify({'api_results': [], 'user_results': []})

        # Split and clean ingredients
        ingredients = [i.strip().lower() for i in ingredients_param.split(',') if i.strip()]
        if not ingredients:
            return jsonify({'api_results': [], 'user_results': []})

        # Search API recipes if API key is available
        api_results = []
        if current_app.config.get('SPOONACULAR_API_KEY'):
            try:
                api_results = MealDBAPI.search_by_ingredients(ingredients)
                current_app.logger.info(f"API search results: {api_results}")
            except Exception as e:
                error_message = str(e)
                current_app.logger.error(f"API Error: {error_message}")
                if hasattr(e, 'code'):
                    if e.code == ErrorCode.AuthenticationError:
                        current_app.logger.error("Invalid API key - disabling API features")
                        current_app.config['SPOONACULAR_API_KEY'] = None
                    elif e.code == ErrorCode.QuotaExceeded:
                        current_app.logger.warning("Daily API quota exceeded")
                        return jsonify({
                            'error': "Daily API limit reached. Only showing community recipes.",
                            'api_results': [],
                            'user_results': []
                        })
                return jsonify({
                    'error': f"API Error: {error_message}",
                    'api_results': [],
                    'user_results': []
                })

        # Search user-submitted recipes
        from sqlalchemy import or_
        user_recipes = Recipe.query\
            .filter(or_(*[
                Recipe.ingredients.contains(ingredient)
                for ingredient in ingredients
            ]))\
            .order_by(Recipe.created_at.desc())\
            .all()

        user_results = []
        for recipe in user_recipes:
            recipe_dict = recipe.to_dict()
            # Split ingredients into lines and clean them
            recipe_ingredients = [line.strip() for line in recipe_dict['ingredients'].lower().split('\n') if line.strip()]
            
            # Calculate matching ingredients with better matching logic
            matching = []
            missing = []
            for ri in recipe_ingredients:
                matched = False
                for ing in ingredients:
                    if ing in ri.lower():
                        matching.append(ri)
                        matched = True
                        break
                if not matched:
                    missing.append(ri)
            
            # Calculate match percentage
            match_percentage = (len(matching) / len(ingredients)) * 100
            
            recipe_dict.update({
                'match_percentage': round(match_percentage, 1),
                'matching_ingredients': matching,
                'missing_ingredients': missing
            })
            user_results.append(recipe_dict)
        
        # Sort by match percentage
        user_results.sort(key=lambda x: x['match_percentage'], reverse=True)

        # Log results for debugging
        current_app.logger.debug(f"API Results: {len(api_results) if api_results else 0} recipes")
        current_app.logger.debug(f"User Results: {len(user_results) if user_results else 0} recipes")
        current_app.logger.debug(f"First API Result: {api_results[0] if api_results else 'None'}")
        current_app.logger.debug(f"First User Result: {user_results[0] if user_results else 'None'}")
        
        # Return results
        response = {
            'api_results': api_results if api_results else [],
            'user_results': user_results if user_results else [],
            'success': True,
            'message': 'Search completed successfully'
        }
        current_app.logger.debug(f"Sending response: {response}")
        return jsonify(response)

    except Exception as e:
        current_app.logger.error(f"Search error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@bp.route('/about')
def about():
    return render_template('main/about.html', title='Über uns')

@bp.route('/impressum')
def impressum():
    return render_template('main/impressum.html', title='Impressum')

@bp.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)
