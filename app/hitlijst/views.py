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
from app.models import User, Song, UserChoice
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
    tracks={}
    if request.method == 'POST' and search_form.validate() and not song_form.song_id.data:
        tracks=search_spotify(search_form.searchfield.data)
        session['tracks']=tracks

        user = User.query.filter_by(first_name=search_form.naam.data).first()
        if not user:
            user = User(first_name=search_form.naam.data)
            db.session.add(user)
            db.session.commit()
        session['user_id']=user.id

    if request.method == 'POST' and song_form.validate() and song_form.song_id.data:
        print song_form.song_id.data
        chosen_song=session['tracks'][song_form.song_id.data]
        song = Song.query.filter_by(id=chosen_song['id']).first()
        if not song:
            song = Song(id=song_form.song_id.data, name=chosen_song['name'], artists=chosen_song['artists'], uri=chosen_song['uri'])
            db.session.add(song)
            db.session.commit()

        user=User.query.filter_by(id=session['user_id']).first()
        user_choise = UserChoice.query.filter_by(user_id=user.id, song_id=song.id).first()
        if not user_choise:
            user_choise = UserChoice(user_id=user.id, song_id=song.id)
            user_choise.rank=user.song_choices_count()
            db.session.add(user_choise)
            db.session.commit()

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

