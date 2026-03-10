'''
Docstring for placement_portal.config
Settings drawer
This is just:

Secret key

Database path

Upload folder


'''

# config.py

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) 


class Config:
    SECRET_KEY = "dev-secret-key"  # change later
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'placement.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "uploads", "resumes")
   # WTF_CSRF_ENABLED = False