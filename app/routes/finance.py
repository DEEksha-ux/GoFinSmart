from flask import flash, Blueprint, render_template, redirect, url_for, session
from app import db
from app.models import FinDetails
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField
from wtforms.validators import InputRequired

class MoneyDetails(FlaskForm):
    amount=IntegerField('Amount', validators=[InputRequired('Amount cannot be empty')])
    type=RadioField('Type', choices=[('expenditure','Expenditure'), ('income','Income')])
    category=StringField('Category')
    submit=SubmitField('Add')

fin_bp=Blueprint(__name__, 'fin')

@fin_bp.route('\view_fin')
def view_fin():
    if 'user' not in session:
        return redirect(url_for('login.login'))
    details=FinDetails.query.all()
    return render_template('view_fin.html', details=details)