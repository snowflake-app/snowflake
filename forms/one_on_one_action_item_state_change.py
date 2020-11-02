from wtforms import HiddenField
from wtforms.validators import DataRequired

from forms.base_form import BaseForm


class OneOnOneActionItemStateChange(BaseForm):
    action_item = HiddenField('', [DataRequired()])
