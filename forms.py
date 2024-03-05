from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, URLField
from wtforms.validators import InputRequired

class AddCupcakeForm(FlaskForm):

    flavor = StringField(
        'Flavor',
        validators=[InputRequired()]
    )

    rating = IntegerField(
        'Rating',
        validators=[InputRequired()]
    )

    size = StringField(
        'Size',
        validators=[InputRequired()]
    )

    image_url = URLField(
        'Image URL',
    )

class EditCupcakeForm(FlaskForm):

    flavor = StringField(
        'Flavor',
    )

    rating = IntegerField(
        'Rating',
    )

    size = StringField(
        'Size',
    )

    image_url = URLField(
        'Image URL',
    )


