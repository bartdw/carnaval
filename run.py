#!/usr/bin/env python
import os
import subprocess

from app import create_app, db
from config import Config

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()