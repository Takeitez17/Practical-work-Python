from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class IndexForm(FlaskForm):
    desc = TextAreaField("Введите описание игры", validators=[DataRequired()])
    submit = SubmitField('Отправить')
    answer = StringField("Жанры")
