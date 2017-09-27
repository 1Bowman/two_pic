from flask_wtf import Form
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class UploadForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(1, 32)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(1, 32)])
    description = TextAreaField('Description of Image', validators=[Length(0, 141)])
    image = FileField('Image', validators=[DataRequired()])

    submit = SubmitField()
