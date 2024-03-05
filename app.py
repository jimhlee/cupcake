"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request, flash, render_template
# from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, Cupcake, db, SQLAlchemy

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

@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Updates cupcake in db and
    returns JSON {"cupcake": {id, flavor, size, ...}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor') or cupcake.flavor
    cupcake.size = request.json.get('size') or cupcake.size
    cupcake.rating = request.json.get('rating') or cupcake.rating
    cupcake.image_url = request.json.get('image_url') or cupcake.image_url or None
    serialized = cupcake.serialize()

    db.session.commit()

    return (jsonify(cupcake=serialized))

@app.delete('/api/cupcakes/<cupcake_id>')
def delete_cupcake(cupcake_id):
    """Deletes cupcake in db and
    returns JSON {"deleted": cupcake_id}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    flash(f'{cupcake.flavor} successfully deleted')
    return jsonify({'deleted': cupcake_id})

@app.get('/')
def show_homepage():
    """Returns HTML for home page."""
    return render_template('homepage.html')


@app.route('/api/cupcakes/search')
def search_cupcakes(search_term):
    all_cupcakes = Cupcake.query.all()
    filtered_cupcakes = []

    for cupcake in all_cupcakes:
        values = cupcake.values()
        if search_term in values:
            filtered_cupcakes.append(cupcake)

    serialized = [c.serialize() for c in filtered_cupcakes]

    return jsonify(cupcakes=serialized)