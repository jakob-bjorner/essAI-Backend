import os

from flask import Flask
from flask_cors import CORS
from models import db
from schemas import ma
from routes import api

herokuPort = int(os.environ.get("PORT", 17995))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
CORS(app)
db.init_app(app)
ma.init_app(app)
api.init_app(app)

if __name__ == '__main__':
	app.run(debug=True, port=herokuPort)
