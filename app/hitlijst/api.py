from flask import (
    Blueprint,
)
from flask_restful import Api, Resource, url_for

from app import api

hitlijst_api = Blueprint('hitlijst_api', __name__)

class SongSearch(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(SongSearch, '/search')


@hitlijst_api.route('/', methods=['GET', 'POST'])
#@login_required
def search():
    form = SearchSongForm()
    return render_template('hitlijst/index.html', form=form)