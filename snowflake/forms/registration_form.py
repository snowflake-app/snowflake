from wtforms import StringField
from wtforms.validators import DataRequired, Length

from .base_form import BaseForm


class RegistrationForm(BaseForm):
    team_name = StringField('Team name', [DataRequired(), Length(min=3, max=255)])
    designation = StringField('Designation', [DataRequired(), Length(min=3, max=255)])
