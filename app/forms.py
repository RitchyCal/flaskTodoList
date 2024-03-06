from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField
from wtforms.validators import DataRequired, length 

class TaskForm(FlaskForm):
	label = TextAreaField('label', validators = [DataRequired()])