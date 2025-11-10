from flask import render_template, url_for, redirect, session, Blueprint, flash
from app import db
from app.models import UserDetails
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class Signup(FlaskForm):
    name=StringField('Name', validators=[InputRequired('Name cannot be empty')])
    password=PasswordField('Password', validators=[InputRequired('Name cannot be empty'), Length(min=6, message='Password must contain at least 6 characters')])
    submit=SubmitField('Submit')

login_bp=Blueprint('login', __name__)

#For first time user
@login_bp.route('/', methods=['GET', 'POST'])
def signup():
    form=Signup()
    if form.validate_on_submit():
        name=form.name.data
        password=form.password.data
        
        existing_user=UserDetails.query.filter_by(name=name).first()
        if (existing_user):
            flash('Entered username already exists. Please choose another name.','danger')
            return redirect(url_for('login.signup'))

        new_user=UserDetails(name=name, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['user']=name
        flash(f"Hi {name}, You have successfully signed in!", "success")
        return redirect(url_for('fin.view_fin'))
    return render_template('home.html', form=form)

#For already registered user logging in again
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form=Signup()
    if form.validate_on_submit():
        name=form.name.data
        password=form.password.data
        
        user=UserDetails.query.filter_by(name=name).first()
        
        if user and user.password==password:
            session['user']=name
            flash(f"Hi {name}, Welcome back!", "success")
            return redirect(url_for('fin.view_fin'))
        else:
            flash("Incorrect name or password, please try again","danger")
            return redirect(url_for('login.login'))
        
    return render_template('login.html', form=form)

@login_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("You logged out successfully", 'success')
    return redirect(url_for('login.login'))
            
            