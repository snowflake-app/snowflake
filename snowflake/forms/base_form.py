from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import DataRequired, Length, Regexp


def infer_html_attrs(field: Field):
    attrs = {}

    if field.flags.required:
        attrs['required'] = True

    if field.description:
        attrs['title'] = field.description

    for validator in field.validators:
        if isinstance(validator, DataRequired):
            attrs['required'] = True
        if isinstance(validator, Length):
            if validator.min > -1:
                attrs['minlength'] = validator.min

            if validator.max > -1:
                attrs['maxlength'] = validator.max
        if isinstance(validator, Regexp):
            attrs['pattern'] = validator.regex.pattern

    return attrs


class BaseForm(FlaskForm):
    class Meta(FlaskForm.Meta):
        def render_field(self, field, render_kw):
            attrs = field.render_kw if field.render_kw else {}
            attrs.update(render_kw)

            html_attrs = infer_html_attrs(field)
            html_attrs.update(attrs)

            return field.widget(field, **html_attrs)
