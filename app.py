"""Flask app for Cupcakes"""
import os

from flask import Flask, jsonify, request, flash, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, Cupcake, db, SQLAlchemy
from forms import AddCupcakeForm, EditCupcakeForm

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
    form = AddCupcakeForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_cupcake = Cupcake(**data)

        db.session.add(new_cupcake)
        db.session.commit()
        flash("Cupcake added.")

        serialized = new_cupcake.serialize()
        return (jsonify(cupcake=serialized), 201)

    else:
        return render_template('homepage.html', form=form)
    # cupcake = Cupcake(
    #     flavor = request.json['flavor'],
    #     size = request.json['size'],
    #     rating = request.json['rating'],
    #     image_url = request.json.get('image_url') or None
    # )

    # db.session.add(cupcake)
    # db.session.commit()



@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Updates cupcake in db and
    returns JSON {"cupcake": {id, flavor, size, ...}}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    form = EditCupcakeForm(obj=cupcake)
    if form.validate_on_submit():
        serialized = cupcake.serialize()

        db.session.commit()
        return (jsonify(cupcake=serialized))

    else:
        return render_template('homepage.html', form=form)
    # cupcake.flavor = request.json.get('flavor') or cupcake.flavor
    # cupcake.size = request.json.get('size') or cupcake.size
    # cupcake.rating = request.json.get('rating') or cupcake.rating
    # cupcake.image_url = request.json.get('image_url') or cupcake.image_url or None




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
def search_cupcakes():
    search_term = request.args['searchTerm']
    filtered_cupcakes = Cupcake.query.filter(Cupcake.flavor.ilike(f'%{search_term}%')).all()

    serialized = [c.serialize() for c in filtered_cupcakes]

    return jsonify(cupcakes=serialized)