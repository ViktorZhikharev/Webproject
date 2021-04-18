from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField 
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта*', validators=[DataRequired()])
    password = PasswordField('Пароль*', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль*', validators=[DataRequired()])
    name = StringField('Имя пользователя*', validators=[DataRequired()])
    phone = StringField('Открытая связь')
    about = TextAreaField("Немного о себе")
    birth = DateField("Дата рождения*")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')