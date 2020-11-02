from wtforms import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length

from forms.base_form import BaseForm


class CommentForm(BaseForm):
    content = TextAreaField('Content', [DataRequired(), Length(max=255)])
    appreciation = HiddenField('', [DataRequired()])
