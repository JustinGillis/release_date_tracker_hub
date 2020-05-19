from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', default=None, validators=[Optional()])
    submit = SubmitField('Submit')