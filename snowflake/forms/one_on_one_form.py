from wtforms import HiddenField
from wtforms.validators import DataRequired, Regexp

from .base_form import BaseForm


class OneOnOneForm(BaseForm):
    user = HiddenField('User', [DataRequired(), Regexp(r'^[\w\-.]+$')])
