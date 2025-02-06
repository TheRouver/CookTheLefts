from app import db, create_app
from app.models import User, Recipe

def remove_test_user():
    app = create_app()
    with app.app_context():
        # Find test user
        test_user = User.query.filter_by(username='test_user').first()
        if not test_user:
            print("Test user not found")
            return

        # Create or get system user
        system_user = User.query.filter_by(username='system').first()
        if not system_user:
            system_user = User(
                username='system',
                email='system@cookthelefts.com'
            )
            system_user.set_password(''.join([chr((x * 64) % 126 + 33) for x in range(16)]))  # Random secure password
            db.session.add(system_user)
            db.session.commit()

        # Transfer recipes to system user
        recipes = Recipe.query.filter_by(user_id=test_user.id).all()
        for recipe in recipes:
            recipe.user_id = system_user.id
        db.session.commit()  # Commit recipe changes first
        
        # Delete test user
        db.session.delete(test_user)
        db.session.commit()  # Then commit user deletion
        
        print(f"Successfully transferred {len(recipes)} recipes to system user and deleted test user")

if __name__ == '__main__':
    remove_test_user()
