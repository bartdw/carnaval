from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from flask_login import current_user, login_required
from flask_rq import get_queue


from app import db
from app.models.user import User
from app.hitlijst.forms import (
    SearchSongForm,
    SongListForm,
)
from .spotify import search_spotify

hitlijst = Blueprint('hitlijst', __name__)


@hitlijst.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    search_form = SearchSongForm()
    song_form = SongListForm()
    tracks=[]
    if request.method == 'POST' and search_form.validate() and not song_form.song_id.data:
        tracks=search_spotify(search_form.searchfield.data)
        session['tracks']=tracks
        naam = search_form.naam.data
        db_naam = User.query.filter_by(first_name=naam).first()
        if not db_naam:
            db_naam = User(first_name=naam)
        db.session.add(db_naam)
        db.session.commit()

    if request.method == 'POST' and song_form.validate() and song_form.song_id.data:
        print song_form.song_id.data
        tracks=session['tracks']

    return render_template('hitlijst/index.html', search_form=search_form, song_form=song_form, tracks=tracks)


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

