
from typing import List, Dict, Optional
import html
from flask import current_app
from enum import Enum
import spoonacular as sp

class ErrorCode(Enum):
    AuthenticationError = "authentication_error"
    QuotaExceeded = "quota_exceeded"
    ApiError = "api_error"
    NetworkError = "network_error"

class McpError(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)

class SpoonacularAPI:
    BASE_URL = "https://api.spoonacular.com"

    @staticmethod
    def get_api_key():
        api_key = current_app.config.get('SPOONACULAR_API_KEY')
        if not api_key:
            raise McpError(ErrorCode.AuthenticationError, "Spoonacular API key not configured")
        return api_key

    @staticmethod
    def _get_api_client():
        """Get an instance of the Spoonacular API client."""
        try:
            api = sp.API(SpoonacularAPI.get_api_key())
            return api
        except Exception as e:
            raise McpError(ErrorCode.AuthenticationError, f"Failed to initialize Spoonacular client: {str(e)}")

    @staticmethod
    def search_by_ingredients(ingredients: List[str]) -> List[Dict]:
        """
        Search for recipes by ingredients using Spoonacular API.
        Returns a list of recipes that contain any of the specified ingredients.
        """
        try:
            api = SpoonacularAPI._get_api_client()
            
            # Clean and validate ingredients
            cleaned_ingredients = [i.strip().lower() for i in ingredients if i.strip()]
            if not cleaned_ingredients:
                return []
            
            # Search for recipes by ingredients
            # Make direct API request
            import requests
            
            url = f"{SpoonacularAPI.BASE_URL}/recipes/findByIngredients"
            params = {
                'apiKey': SpoonacularAPI.get_api_key(),
                'ingredients': ','.join(cleaned_ingredients),
                'number': 10,
                'ranking': 2,
                'ignorePantry': True
            }
            
            response = requests.get(url, params=params)
            current_app.logger.info(f"Raw API response: {response.text}")
            
            if response.status_code == 401:
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif response.status_code == 402:
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            elif response.status_code != 200:
                raise McpError(ErrorCode.ApiError, f"API request failed with status {response.status_code}")
                
            response_data = response.json()
            current_app.logger.info(f"JSON response: {response_data}")
            
            if not response_data:
                current_app.logger.warning("No recipes found for ingredients")
                return []

            detailed_recipes = []
            for recipe in response_data:
                try:
                    # Get detailed recipe information including instructions
                    recipe_details = SpoonacularAPI.get_meal_by_id(str(recipe['id']))
                    if recipe_details:
                        # Get matching ingredients from the initial search response
                        matching_ingredients = []
                        for ing in recipe.get('usedIngredients', []):
                            if ing.get('original'):
                                matching_ingredients.append(ing.get('original'))
                            elif ing.get('amount') and ing.get('unit') and ing.get('name'):
                                matching_ingredients.append(f"{ing.get('amount')} {ing.get('unit')} {ing.get('name')}")
                        
                        # Get missing ingredients
                        missing_ingredients = []
                        for ing in recipe.get('missedIngredients', []):
                            if ing.get('original'):
                                missing_ingredients.append(ing.get('original'))
                            elif ing.get('amount') and ing.get('unit') and ing.get('name'):
                                missing_ingredients.append(f"{ing.get('amount')} {ing.get('unit')} {ing.get('name')}")

                        # Log ingredients for debugging
                        current_app.logger.info(f"Matching ingredients: {matching_ingredients}")
                        current_app.logger.info(f"Missing ingredients: {missing_ingredients}")

                        # Calculate match percentage
                        used_count = len(recipe.get('usedIngredients', []))
                        missed_count = len(recipe.get('missedIngredients', []))
                        total_count = used_count + missed_count
                        match_percentage = (used_count / total_count * 100) if total_count > 0 else 0
                        
                        # Update recipe details with matching info
                        recipe_details['matching_ingredients'] = []
                        recipe_details['missing_ingredients'] = []
                        
                        # Add ingredients with proper formatting
                        for ing in matching_ingredients:
                            recipe_details['matching_ingredients'].append(str(ing))
                        for ing in missing_ingredients:
                            recipe_details['missing_ingredients'].append(str(ing))
                            
                        recipe_details['match_percentage'] = match_percentage
                        
                        # Log the recipe details for debugging
                        current_app.logger.info(f"Recipe details: {recipe_details}")
                        
                        detailed_recipes.append(recipe_details)
                except Exception as e:
                    current_app.logger.error(f"Error processing recipe {recipe.get('id')}: {str(e)}")
                    continue
            
            # Sort by match percentage
            detailed_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
            return detailed_recipes
                
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                current_app.logger.error("API Authentication failed - invalid API key")
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif "402" in error_msg:
                current_app.logger.error("API quota exceeded")
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            else:
                current_app.logger.error(f"Error searching for recipes: {error_msg}")
                raise McpError(ErrorCode.ApiError, f"API request failed: {error_msg}")
        return []

    @staticmethod
    def get_meal_by_id(recipe_id: str) -> Optional[Dict]:
        """Get detailed information about a specific recipe."""
        try:
            import requests
            
            url = f"{SpoonacularAPI.BASE_URL}/recipes/{recipe_id}/information"
            params = {
                'apiKey': SpoonacularAPI.get_api_key()
            }
            
            response = requests.get(url, params=params)
            current_app.logger.info(f"Recipe info response: {response.text}")
            
            if response.status_code == 401:
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif response.status_code == 402:
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            elif response.status_code != 200:
                raise McpError(ErrorCode.ApiError, f"API request failed with status {response.status_code}")
                
            recipe = response.json()
            if recipe:
                return SpoonacularAPI._format_meal_data(recipe)
            return None
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                current_app.logger.error("API Authentication failed - invalid API key")
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif "402" in error_msg:
                current_app.logger.error("API quota exceeded")
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            else:
                current_app.logger.error(f"Error fetching recipe {recipe_id}: {error_msg}")
                raise McpError(ErrorCode.ApiError, f"API request failed: {error_msg}")

    @staticmethod
    def get_random_meals(count: int = 6) -> List[Dict]:
        """Get a list of random recipes."""
        try:
            import requests
            
            url = f"{SpoonacularAPI.BASE_URL}/recipes/random"
            params = {
                'apiKey': SpoonacularAPI.get_api_key(),
                'number': count * 2  # Request more to account for potential formatting errors
            }
            
            response = requests.get(url, params=params)
            current_app.logger.info(f"Random recipes response: {response.text}")
            
            if response.status_code == 401:
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif response.status_code == 402:
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            elif response.status_code != 200:
                raise McpError(ErrorCode.ApiError, f"API request failed with status {response.status_code}")
                
            response_data = response.json()
            if not response_data:
                return []
                
            recipes = response_data.get('recipes', [])
            formatted_recipes = []
            for recipe in recipes:
                try:
                    formatted_recipe = SpoonacularAPI._format_meal_data(recipe)
                    if formatted_recipe:
                        formatted_recipes.append(formatted_recipe)
                        if len(formatted_recipes) >= count:
                            break
                except Exception as e:
                    current_app.logger.error(f"Error formatting recipe: {str(e)}")
                    continue
            
            return formatted_recipes
                
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                current_app.logger.error("API Authentication failed - invalid API key")
                raise McpError(ErrorCode.AuthenticationError, "Invalid API key")
            elif "402" in error_msg:
                current_app.logger.error("API quota exceeded")
                raise McpError(ErrorCode.QuotaExceeded, "Daily API quota exceeded")
            else:
                current_app.logger.error(f"Error fetching random recipes: {error_msg}")
                raise McpError(ErrorCode.ApiError, f"API request failed: {error_msg}")
        
        return []

    @staticmethod
    def _format_meal_data(recipe: Dict) -> Optional[Dict]:
        """Format the recipe data into a consistent structure."""
        try:
            if not recipe or not isinstance(recipe, dict):
                return None

            # Extract ingredients with measures
            ingredients = []
            for ingredient in recipe.get('extendedIngredients', []):
                name = ingredient.get('name', '').strip()
                measure = ingredient.get('original', '').strip()
                if name and measure:
                    ingredients.append({
                        'ingredient': name,
                        'measure': measure,
                        'amount': ingredient.get('amount', 0),
                        'unit': ingredient.get('unit', '')
                    })

            # Process instructions more robustly
            instructions = []
            if recipe.get('analyzedInstructions'):
                for instruction in recipe['analyzedInstructions']:
                    for step in instruction.get('steps', []):
                        step_text = step.get('step', '').strip()
                        if step_text:
                            instructions.append(html.unescape(step_text))
            elif recipe.get('instructions'):
                # Better splitting for raw instructions
                raw_steps = recipe['instructions'].split('.')
                instructions = [html.unescape(step.strip()) 
                              for step in raw_steps 
                              if step.strip()]

            # Enhanced metadata
            dish_types = recipe.get('dishTypes', [])
            cuisines = recipe.get('cuisines', [])
            diets = recipe.get('diets', [])
            
            return {
                'id': str(recipe.get('id', '')),
                'title': html.unescape(recipe.get('title', '')),
                'category': dish_types[0].capitalize() if dish_types else 'Main Course',
                'area': cuisines[0] if cuisines else 'International',
                'instructions': instructions if instructions else ['No instructions available.'],
                'image_url': recipe.get('image', ''),
                'youtube_url': recipe.get('videoUrl', '') if recipe.get('videoUrl', '').startswith('https://') else '',
                'ingredients': ingredients if ingredients else [{'ingredient': 'No ingredients available', 'measure': '', 'amount': 0, 'unit': ''}],
                'source': recipe.get('sourceUrl', ''),
                'ready_in_minutes': recipe.get('readyInMinutes', 0),
                'servings': recipe.get('servings', 0),
                'tags': list(set(dish_types + cuisines + diets)),
                'vegetarian': recipe.get('vegetarian', False),
                'vegan': recipe.get('vegan', False),
                'gluten_free': recipe.get('glutenFree', False),
                'dairy_free': recipe.get('dairyFree', False)
            }
        except Exception as e:
            current_app.logger.error(f"Error formatting recipe data: {str(e)}")
            return None

# Use SpoonacularAPI as MealDBAPI for backwards compatibility
MealDBAPI = SpoonacularAPI
