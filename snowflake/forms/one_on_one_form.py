from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

from .base_form import BaseForm


class OneOnOneForm(BaseForm):
    user = StringField('User', [DataRequired(), Regexp(r'^[\w\-.]+$')])
