from flask import Flask
from config import settings
from models import db


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

@app.route("/")
def home():
  return "Food Listing Page"

@app.route("/donate", methods=['POST', 'GET'])
def donate():
  return "Donation Page"



if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
