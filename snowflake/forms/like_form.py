from wtforms import HiddenField
from wtforms.validators import DataRequired

from .base_form import BaseForm


class LikeForm(BaseForm):
    appreciation = HiddenField('', [DataRequired()])
