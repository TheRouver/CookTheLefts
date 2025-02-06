from app import db, create_app
from app.models import User, Recipe

def create_test_data():
    app = create_app()
    with app.app_context():
        # Create test user if not exists
        user = User.query.filter_by(username='test_user').first()
        if not user:
            user = User(username='test_user', email='test@example.com')
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()
        
        # Create test recipe
        recipe = Recipe(
            title='Test Potato Recipe',
            ingredients='2 large potatoes\n1 onion\nsalt and pepper',
            instructions='1. Peel and cut potatoes\n2. Cook until tender',
            user_id=user.id
        )
        db.session.add(recipe)
        db.session.commit()
        print('Test recipe created successfully')

if __name__ == '__main__':
    create_test_data()
