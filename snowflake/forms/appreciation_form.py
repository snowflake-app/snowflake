from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length

from .base_form import BaseForm


class AppreciationForm(BaseForm):
    content = TextAreaField('Content', [DataRequired(), Length(max=255)])
