from wtforms import HiddenField
from wtforms.validators import DataRequired

from forms.base_form import BaseForm


class LikeForm(BaseForm):
    appreciation = HiddenField('', [DataRequired()])
