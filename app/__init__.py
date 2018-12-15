import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up spotify connection
    client_credentials_manager = SpotifyClientCredentials(app.config['SPOTIFY_ID'], app.config['SPOTIFY_SECRET'])
    app.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    config[config_name].init_app(app)

    # Set up extensions
    db.init_app(app)

    # Create app blueprints
    from .hitlijst import hitlijst as hitlijst_blueprint
    app.register_blueprint(hitlijst_blueprint, url_prefix='/hitlijst')

    return app

