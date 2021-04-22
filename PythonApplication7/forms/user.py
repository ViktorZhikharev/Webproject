from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Optional


class RegisterForm(FlaskForm):
    email = EmailField('Почта*', validators=[DataRequired()])
    password = PasswordField('Пароль*', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль*', validators=[DataRequired()])
    name = StringField('Имя пользователя*', validators=[DataRequired()])
    phone = StringField('Открытая связь')
    about = TextAreaField("Немного о себе")
    birth = DateField("Дата рождения", validators=(Optional(),))
    submit = SubmitField('Зарегистрироваться')


class EditForm(FlaskForm):
    password = PasswordField('Пароль', default=None)
    password_again = PasswordField('Повторите пароль', default=None)
    name = StringField('Имя пользователя', default=None)
    phone = StringField('Открытая связь', default=None)
    about = TextAreaField("Немного о себе", default=None)
    birth = DateField("Дата рождения", default=None, validators=(Optional(),))
    submit = SubmitField('Применить изменения', default=None)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')