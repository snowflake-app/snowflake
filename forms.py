from wtforms import Form, StringField, validators, TextAreaField, HiddenField


class RegistrationForm(Form):
    team_name = StringField('Team Name', [validators.DataRequired(), validators.Length(min=3, max=25)])
    designation = StringField('Designation', [validators.DataRequired(), validators.Length(min=3, max=25)])


class AppreciationForm(Form):
    content = TextAreaField('Content', [validators.DataRequired(), validators.Length(min=1, max=255)])


class LikeForm(Form):
    appreciation = HiddenField('Appreciation', [validators.DataRequired()])
