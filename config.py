import os

from dotenv import load_dotenv

load_dotenv('variables.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///travel_routes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
