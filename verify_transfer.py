from app import db, create_app
from app.models import User, Recipe

def verify_transfer():
    app = create_app()
    with app.app_context():
        # Verify test user is gone
        test_user = User.query.filter_by(username='test_user').first()
        if test_user:
            print("Error: Test user still exists")
            return

        # Verify system user has the recipe
        system_user = User.query.filter_by(username='system').first()
        if not system_user:
            print("Error: System user not found")
            return

        recipes = Recipe.query.filter_by(user_id=system_user.id).all()
        if not recipes:
            print("Error: No recipes found under system user")
            return

        print("Verification successful:")
        for recipe in recipes:
            print(f"Recipe '{recipe.title}' is now owned by system user")

if __name__ == '__main__':
    verify_transfer()
