from wtforms import Form, StringField, validators, TextAreaField, HiddenField, BooleanField


class RegistrationForm(Form):
    team_name = StringField('Team Name', [validators.DataRequired(), validators.Length(min=3, max=25)])
    designation = StringField('Designation', [validators.DataRequired(), validators.Length(min=3, max=25)])


class AppreciationForm(Form):
    content = TextAreaField('Content', [validators.DataRequired(), validators.Length(min=1, max=255)])


class LikeForm(Form):
    appreciation = HiddenField('Appreciation', [validators.DataRequired()])


class CommentForm(Form):
    content = TextAreaField('Content', [validators.DataRequired(), validators.Length(min=1, max=255)])
    appreciation = HiddenField('Appreciation', [validators.DataRequired()])


class OneOnOneForm(Form):
    user = TextAreaField('User', [validators.DataRequired()])


class OneOnOneActionItemForm(Form):
    content = StringField('Content', [validators.DataRequired()])
    one_on_one = HiddenField('')
