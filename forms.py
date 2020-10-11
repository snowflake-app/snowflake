from wtforms import Form, StringField, validators, TextAreaField, HiddenField


class RegistrationForm(Form):
    team_name = StringField('Team Name', [validators.DataRequired(), validators.Length(min=3, max=255)])
    designation = StringField('Designation', [validators.DataRequired(), validators.Length(min=3, max=255)])


class AppreciationForm(Form):
    content = TextAreaField('Content', [validators.DataRequired(), validators.Length(min=1, max=255)])


class LikeForm(Form):
    appreciation = HiddenField('Appreciation', [validators.DataRequired()])


class CommentForm(Form):
    content = TextAreaField('Content', [validators.DataRequired(), validators.Length(min=1, max=255)])
    appreciation = HiddenField('Appreciation', [validators.DataRequired()])


class OneOnOneForm(Form):
    user = StringField('User', [validators.DataRequired()])


class OneOnOneActionItemForm(Form):
    content = StringField('Content', [validators.DataRequired()])
    one_on_one = HiddenField('')


class OneOnOneActionItemDone(Form):
    action_item = HiddenField('', [validators.DataRequired()])
