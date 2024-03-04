"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request
# from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cupcake, db

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
    """Return JSON {"cupcakes": [{id, flavor, size, ...}, ...]}"""
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def show_cupcake(cupcake_id):
    """Returns JSON {"cupcake": {id, flavor, size, ...}}."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post('/api/cupcakes')
def new_cupcake():
    """Creates new cupcake in db and
    returns JSON {"cupcake": {id, flavor, size, ...}}."""
    cupcake = Cupcake(
        flavor = request.json['flavor'],
        size = request.json['size'],
        rating = request.json['rating'],
        image_url = request.json.get('image_url') or None
    )

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)
