from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class SignupForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    image_url = StringField('Image URL (Optional)')


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField('Current Password', validators=[InputRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[InputRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[InputRequired(), Length(min=6)])