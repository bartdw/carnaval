from flask_wtf import Form
from wtforms.fields import (
    PasswordField,
    StringField,
    SubmitField,
    HiddenField
)

class SearchSongForm(Form):
    naam = StringField('Naam...')
    searchfield = StringField('Zoek liedje...')
    submit = SubmitField('Zoek')

class SongListForm(Form):
    song_id = HiddenField('song...')