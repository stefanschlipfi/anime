
#! /bin/bash

source /opt/python-venv/anime-venv/bin/activate
export FLASK_APP=/opt/anime/backend/flask_app.py

export PATH=$PATH:/opt/anime/backend
flask run --host 0.0.0.0 --port=7080