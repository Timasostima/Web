from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, Optional, Length, ValidationError, Email
from app.models import User


class RegisterForm(FlaskForm):

    email = EmailField(validators=[InputRequired(), Length(min=4, max=30), Email()], render_kw={"placeholder": "Email"})
    name = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Name"})
    last_name = StringField(validators=[Optional(), Length(min=3, max=30)], render_kw={"placeholder": "Lastname"})
    company_name = StringField(validators=[Optional(), Length(min=3, max=20)], render_kw={"placeholder": "Company Name"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('Email already taken')


class LoginForm(FlaskForm):
    email = EmailField(validators=[InputRequired(), Length(min=4, max=30), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')
