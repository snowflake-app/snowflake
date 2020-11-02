from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

from forms.base_form import BaseForm


class OneOnOneActionItemForm(BaseForm):
    content = StringField('Content', [DataRequired()])
    one_on_one = HiddenField('')
