from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Optional

class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class MovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired()])
    timestamp = DateTimeField('Timestamp (optional, YYYY-mm-dd HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    product_id = SelectField('Product', validators=[DataRequired()], choices=[])
    from_location = SelectField('From Location (leave blank if inbound)', validators=[Optional()], choices=[])
    to_location = SelectField('To Location (leave blank if outbound)', validators=[Optional()], choices=[])
    qty = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Record')
