from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, StringField, SubmitField, SelectField

"""
AUTHORS

Trish Beeksma
Alex Mello
Matthew Siebold
"""


class newItem(FlaskForm):
    name = StringField('Item Name')
    restaurantID = SelectField('Restaurant ID', choices=[])
    price = FloatField('Price')
    calories = IntegerField('Calories')
    fat = IntegerField('Fat')
    carbs = IntegerField('Carbs')
    protein = IntegerField('Protein')
    foodType = SelectField('Food Type', choices=[])
    submit = SubmitField('Submit')


class newCombination(FlaskForm):
    comboName = StringField('Combination Name')
    comborestaurantID = SelectField('Restaurant ID', choices=[])
    submitCombo = SubmitField('Submit')


class comboItem(FlaskForm):
    itemOne = SelectField('Item One', choices=[])
    itemTwo = SelectField('Item Two', choices=[])
    itemThree = SelectField('Item Three', choices=[])
    submitComboItem = SubmitField('Submit')


class rollBack(FlaskForm):
    rollback = SubmitField('Rollback Changes')


class commitChange(FlaskForm):
    commit = SubmitField('Commit Changes')
