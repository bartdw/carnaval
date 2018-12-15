from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_rq import get_queue

from app import db
from app.hitlijst.forms import (
    SearchSongForm
)
from .spotify import search_spotify

hitlijst = Blueprint('hitlijst', __name__)


@hitlijst.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    form = SearchSongForm()
    tracks=[]
    if request.method == 'POST' and form.validate():
        tracks=search_spotify(form.searchfield.data)

    return render_template('hitlijst/index.html', form=form, tracks=tracks)


@hitlijst.route('/new-user', methods=['GET', 'POST'])
@login_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('admin/new_user.html', form=form)

