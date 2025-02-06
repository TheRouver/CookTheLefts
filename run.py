from app import create_app, db
from app.models import User, Recipe, Like

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Recipe': Recipe,
        'Like': Like
    }

if __name__ == '__main__':
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()
    app.run(debug=True)
