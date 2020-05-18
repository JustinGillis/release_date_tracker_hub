from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField

class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', default=None, validators=[Optional()])
    submit = SubmitField('Submit')