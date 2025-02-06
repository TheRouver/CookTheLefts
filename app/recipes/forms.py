from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class RecipeForm(FlaskForm):
    title = StringField('Titel', validators=[
        DataRequired(message='Bitte geben Sie einen Titel ein'),
        Length(min=3, max=100, message='Der Titel muss zwischen 3 und 100 Zeichen lang sein')
    ])
    
    ingredients = TextAreaField('Zutaten (eine pro Zeile)', validators=[
        DataRequired(message='Bitte geben Sie die Zutaten ein'),
        Length(min=10, message='Bitte geben Sie mindestens eine Zutat ein')
    ])
    
    instructions = TextAreaField('Zubereitungsanleitung', validators=[
        DataRequired(message='Bitte geben Sie eine Zubereitungsanleitung ein'),
        Length(min=30, message='Die Anleitung sollte ausführlicher sein (mindestens 30 Zeichen)')
    ])
    
    image = FileField('Bild hochladen', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Nur Bilder sind erlaubt!')
    ])
    
    video_link = StringField('Video Link (optional)', validators=[
        Length(max=500, message='Der Video Link darf maximal 500 Zeichen lang sein')
    ])
    
    submit = SubmitField('Rezept speichern')

    def validate_ingredients(self, field):
        # Ensure each ingredient is on a new line and properly formatted
        ingredients = field.data.split('\n')
        cleaned_ingredients = []
        for ingredient in ingredients:
            ingredient = ingredient.strip()
            if ingredient:  # Only add non-empty lines
                cleaned_ingredients.append(ingredient)
        field.data = '\n'.join(cleaned_ingredients)

    def validate_instructions(self, field):
        # Clean up instructions formatting
        instructions = field.data.split('\n')
        cleaned_instructions = []
        for instruction in instructions:
            instruction = instruction.strip()
            if instruction:  # Only add non-empty lines
                cleaned_instructions.append(instruction)
        field.data = '\n'.join(cleaned_instructions)

class CommentForm(FlaskForm):
    content = TextAreaField('Kommentar', validators=[
        DataRequired(message='Bitte geben Sie einen Kommentar ein'),
        Length(min=1, max=500, message='Der Kommentar muss zwischen 1 und 500 Zeichen lang sein')
    ])
    rating = IntegerField('Bewertung (1-10)', validators=[
        DataRequired(message='Bitte geben Sie eine Bewertung ab'),
        NumberRange(min=1, max=10, message='Die Bewertung muss zwischen 1 und 10 liegen')
    ])
    submit = SubmitField('Kommentar abschicken')
