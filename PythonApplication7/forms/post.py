from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Введите название', validators=[DataRequired()])
    text = TextAreaField('Введите текст зесь', validators=[DataRequired()])
    submit = SubmitField('Запостить')

class CommentForm(FlaskForm):
    text = TextAreaField('Введите текст зесь', validators=[DataRequired()])
    submit = SubmitField('Запостить')

class MessageForm(FlaskForm):
    text = TextAreaField('Введите текст зесь', validators=[DataRequired()])
    submit = SubmitField('Написать сообщение')