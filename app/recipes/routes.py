import os
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify, send_from_directory
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app import db
from app.recipes import bp
from app.models import Recipe, Like, Comment
from app.recipes.forms import RecipeForm, CommentForm
from app.services.meal_api import MealDBAPI
from datetime import datetime
import uuid

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(form_image):
    if form_image:
        filename = secure_filename(form_image.filename)
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}_{filename}"
        # Create uploads directory if it doesn't exist
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        # Save file
        filepath = os.path.join(upload_folder, unique_filename)
        form_image.save(filepath)
        return f"uploads/{unique_filename}"  # Return URL-friendly path
    return None

def delete_image(image_path):
    if image_path:
        try:
            full_path = os.path.join(current_app.root_path, 'static', image_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            current_app.logger.error(f"Error deleting image {image_path}: {e}")

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()
    if form.validate_on_submit():
        try:
            image_path = save_image(form.image.data) if form.image.data else None
            
            recipe = Recipe(
                title=form.title.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                image_path=image_path,
                video_link=form.video_link.data,
                author=current_user
            )
            
            db.session.add(recipe)
            db.session.commit()
            
            flash('Your recipe has been created successfully!', 'success')
            return redirect(url_for('recipes.view', id=recipe.id))
        except Exception as e:
            if image_path:
                delete_image(image_path)
            flash('An error occurred while creating the recipe.', 'error')
            current_app.logger.error(f"Error creating recipe: {e}")
            return redirect(url_for('recipes.create'))
        
    return render_template('recipes/create.html', 
                         title='Create New Recipe',
                         form=form)

@bp.route('/<id>', methods=['GET', 'POST'])
def view(id):
    source = request.args.get('source', 'user')
    
    if source == 'api':
        # Get recipe from API
        recipe = MealDBAPI.get_meal_by_id(id)
        if recipe:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(recipe)
            return render_template('recipes/view_api.html',
                                title=recipe['title'],
                                recipe=recipe)
        flash('Recipe not found.', 'error')
        return redirect(url_for('main.index'))
    else:
        # Get user-submitted recipe
        recipe = Recipe.query.get_or_404(id)
        form = CommentForm()
        
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash('Sie müssen angemeldet sein, um einen Kommentar zu hinterlassen.', 'error')
                return redirect(url_for('auth.login'))
                
            # Check if user already commented
            existing_comment = Comment.query.filter_by(
                user_id=current_user.id,
                recipe_id=recipe.id
            ).first()
            
            if existing_comment:
                flash('Sie haben bereits einen Kommentar für dieses Rezept abgegeben.', 'error')
                return redirect(url_for('recipes.view', id=id))

            # Validate rating
            if not Comment.validate_rating(form.rating.data):
                flash('Die Bewertung muss zwischen 1 und 10 liegen.', 'error')
                return redirect(url_for('recipes.view', id=id))

            try:
                comment = Comment(
                    content=form.content.data,
                    rating=form.rating.data,
                    user=current_user,
                    recipe=recipe
                )
                db.session.add(comment)
                db.session.commit()
                flash('Ihr Kommentar wurde erfolgreich hinzugefügt!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.', 'error')
                current_app.logger.error(f"Error adding comment: {e}")
            
            return redirect(url_for('recipes.view', id=id))
            
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(recipe.to_dict())
            
        comments = recipe.comments.order_by(Comment.created_at.desc()).all()
        average_rating = recipe.get_average_rating()
        
        return render_template('recipes/view.html',
                             title=recipe.title,
                             recipe=recipe,
                             form=form,
                             comments=comments,
                             average_rating=average_rating)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash('You can only edit your own recipes.', 'error')
        return redirect(url_for('recipes.view', id=id))
    
    form = RecipeForm()
    if form.validate_on_submit():
        try:
            recipe.title = form.title.data
            recipe.ingredients = form.ingredients.data
            recipe.instructions = form.instructions.data
            recipe.video_link = form.video_link.data
            
            if form.image.data:
                # Delete old image if it exists
                old_image_path = recipe.image_path
                new_image_path = save_image(form.image.data)
                
                if new_image_path:
                    recipe.image_path = new_image_path
                    if old_image_path:
                        delete_image(old_image_path)
            
            db.session.commit()
            flash('Your recipe has been updated successfully!', 'success')
            return redirect(url_for('recipes.view', id=id))
        except Exception as e:
            flash('An error occurred while updating the recipe.', 'error')
            current_app.logger.error(f"Error updating recipe: {e}")
            return redirect(url_for('recipes.edit', id=id))
    
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.ingredients.data = recipe.ingredients
        form.instructions.data = recipe.instructions
        form.video_link.data = recipe.video_link
    
    return render_template('recipes/edit.html',
                         title=f'Edit Recipe: {recipe.title}',
                         form=form,
                         recipe=recipe)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author != current_user:
        flash('You can only delete your own recipes.', 'error')
        return redirect(url_for('recipes.view', id=id))
    
    try:
        # Delete image if it exists
        if recipe.image_path:
            delete_image(recipe.image_path)
        
        db.session.delete(recipe)
        db.session.commit()
        flash('Your recipe has been deleted successfully.', 'success')
    except Exception as e:
        flash('An error occurred while deleting the recipe.', 'error')
        current_app.logger.error(f"Error deleting recipe: {e}")
    
    return redirect(url_for('main.index'))

@bp.route('/<int:id>/like', methods=['POST'])
@login_required
def like(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.author == current_user:
        return jsonify({'error': 'You cannot like your own recipe'}), 400
    
    like = Like.query.filter_by(user=current_user, recipe=recipe).first()
    
    if like is None:
        like = Like(user=current_user, recipe=recipe)
        db.session.add(like)
        action = 'liked'
    else:
        db.session.delete(like)
        action = 'unliked'
    
    db.session.commit()
    return jsonify({
        'action': action,
        'likes_count': recipe.likes.count()
    })

@bp.route('/my-recipes')
@login_required
def my_recipes():
    page = request.args.get('page', 1, type=int)
    recipes = Recipe.query.filter_by(author=current_user)\
        .order_by(Recipe.created_at.desc())\
        .paginate(page=page, per_page=12, error_out=False)
    
    return render_template('recipes/my_recipes.html',
                         title='My Recipes',
                         recipes=recipes)

@bp.route('/my-interactions')
@login_required
def my_interactions():
    # Get liked recipes
    liked_recipes = Recipe.query.join(Like)\
        .filter(Like.user_id == current_user.id)\
        .order_by(Recipe.created_at.desc()).all()
    
    # Get rated recipes
    rated_recipes = Recipe.query.join(Comment)\
        .filter(Comment.user_id == current_user.id)\
        .order_by(Recipe.created_at.desc()).all()
    
    return render_template('recipes/my_interactions.html',
                         title='Meine Interaktionen',
                         liked_recipes=liked_recipes,
                         rated_recipes=rated_recipes)
