from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""Models for Cupcake app."""
class Cupcake(db.Model):
    '''Cupcake model'''

    __tablename__ = 'cupcakes'

    def serialize(self):
        """Serialize to dictionary."""
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image_url': self.image_url
        }

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    flavor = db.Column(
        db.String(50),
        nullable = False
    )

    size = db.Column(
        db.String(15),
        nullable = False
    )

    rating = db.Column(
        db.Integer,
        nullable = False
    )

    image_url = db.Column(
        db.String(500),
        default = 'https://tinyurl.com/demo-cupcake',
        nullable = False
    )

    db.CheckConstraint(rating <= 10)

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)