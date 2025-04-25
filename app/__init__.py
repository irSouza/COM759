from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r'/*': {'origins': '*'}})

mongodb_client = PyMongo(app, uri="mongodb+srv://igor:igor@cluster0.upqn1.mongodb.net/igordb?retryWrites=true&w=majority")
db = mongodb_client.db

from app import routes