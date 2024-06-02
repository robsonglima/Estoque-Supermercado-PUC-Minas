from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:senha123@localhost:27017/"
mongo = MongoClient(app.config["MONGO_URI"])

from app_estoque import routes
