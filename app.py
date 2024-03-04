"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cupcake

app = Flask(__name__)
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///cupcake')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# debug = DebugToolbarExtension(app)


@app.get('/api/cupcakes')
def show_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)
