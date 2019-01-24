from flask_wtf import Form
from wtforms.fields import StringField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, url

class RecordForm(Form):
    url = URLField('url', validators=[DataRequired(), url()])
    description = StringField('description')
