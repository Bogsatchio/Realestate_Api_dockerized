from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange,  Length  # pip install email-validator
import pandas as pd

from utils.sqls import sql_get_cities_data
#from db import db


class DownloadsForm(FlaskForm):
    def __init__(self, db, *args, **kwargs):
        super(DownloadsForm, self).__init__(*args, **kwargs)

        # Zaczytanie danych z bazy dot miast oraz min i max rozmiarów mieszkań
        df = pd.read_sql(sql_get_cities_data, db.engine)
        df.set_index("city", inplace=True)
        cities_dict = df.to_dict(orient="index")
        cities_list = [(x, x) for x in list(cities_dict.keys())]

        # Set up choices for dropdown fields
        self.format_dropdown.choices = [('json', 'JSON'), ('csv', 'CSV')]
        self.city_dropdown.choices = cities_list
        self.type_dropdown.choices = [('all', 'Entire data'), ('latest', 'Latest search'), ('prices_over_time', "Prices over time"), ('price_change', 'Price change')]

    #(value_to_submit, value_displayed)
    format_dropdown = SelectField('File Format')
    city_dropdown = SelectField('File Format')
    min_size = DecimalField("min_size", validators=[NumberRange(min=30, max=100, message='Value must be between 30 and 100')])
    max_size = DecimalField("max_size", validators=[NumberRange(min=30, max=100, message='Value must be between 30 and 100')])
    type_dropdown = SelectField('Type of data')
    submit = SubmitField(label="Download")

