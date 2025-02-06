# CookTheLefts

A web application for sharing and discovering recipes.

## System Requirements

### Windows
- Python 3.8 - 3.11 (getestet auf 3.8, 3.9, 3.10, 3.11)
- Visual Studio Code
- Git (optional, für Versionskontrolle)
- Windows 10/11

### macOS
- Python 3.11
- Xcode Command Line Tools
- Visual Studio Code
- Git (optional)
- macOS 11 (Big Sur) oder höher

## Deployment to Render.com

### Prerequisites

1. Create a [Render.com](https://render.com) account
2. Create a [GitHub](https://github.com) account and push your code to a repository

### Deployment Steps

1. Log in to your Render.com account
2. Click on "New +" and select "Web Service"
3. Connect your GitHub repository
4. Use the following settings:
   - Name: cookthelefts (or your preferred name)
   - Environment: Python
   - Build Command: `./build.sh`
   - Start Command: `gunicorn "app:create_app('production')" --bind 0.0.0.0:$PORT`
   - Instance Type: Free (or your preferred tier)

5. Add the following environment variables:
   - `FLASK_ENV`: production
   - `SECRET_KEY`: (will be auto-generated)
   - `SPOONACULAR_API_KEY`: (your API key)

6. Click "Create Web Service"

The application will be automatically deployed and a PostgreSQL database will be created and connected. The database migrations will run automatically during deployment.

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
```

4. Run migrations:
```bash
flask db upgrade
```

5. Run the application:
```bash
python run.py
```

The application will be available at http://localhost:5000
