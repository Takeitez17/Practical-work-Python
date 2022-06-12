import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms import BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    team_leader = IntegerField('ID Тим Лидера', validators=[DataRequired()])
    job = StringField('Название работы', validators=[DataRequired()])
    work_size = IntegerField('Время на выполнение работы', validators=[DataRequired()])
    collaborators = StringField("ID участников", validators=[DataRequired()])
    categories = StringField("ID Категорий", validators=[DataRequired()])
    start_date = DateField("Начало работы", default=datetime.datetime.now)
    end_date = DateField("Конеч работы", default=None)
    is_finished = BooleanField("Завершена работа?")

    submit = SubmitField('Зарегестрироваться')
