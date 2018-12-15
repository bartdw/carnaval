from flask_wtf import Form
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
)

class SearchSongForm(Form):
    searchfield = StringField('Zoek liedje...')
    submit = SubmitField('Zoek')