from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[
        DataRequired(message='E-Mail ist erforderlich'),
        Email(message='Bitte geben Sie eine gültige E-Mail-Adresse ein')
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(message='Passwort ist erforderlich')
    ])
    remember_me = BooleanField('Angemeldet bleiben')
    submit = SubmitField('Anmelden')

class RegistrationForm(FlaskForm):
    username = StringField('Benutzername', validators=[
        DataRequired(message='Benutzername ist erforderlich'),
        Length(min=3, max=64, message='Benutzername muss zwischen 3 und 64 Zeichen lang sein')
    ])
    email = StringField('E-Mail', validators=[
        DataRequired(message='E-Mail ist erforderlich'),
        Email(message='Bitte geben Sie eine gültige E-Mail-Adresse ein'),
        Length(max=120, message='E-Mail darf maximal 120 Zeichen lang sein')
    ])
    password = PasswordField('Passwort', validators=[
        DataRequired(message='Passwort ist erforderlich'),
        Length(min=6, message='Passwort muss mindestens 6 Zeichen lang sein')
    ])
    password2 = PasswordField('Passwort wiederholen', validators=[
        DataRequired(message='Bitte wiederholen Sie Ihr Passwort'),
        EqualTo('password', message='Passwörter müssen übereinstimmen')
    ])
    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Dieser Benutzername ist bereits vergeben.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Diese E-Mail-Adresse wird bereits verwendet.')
