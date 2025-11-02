from flask import flash, Blueprint, render_template, redirect, url_for, session
from app import db
from app.models import FinDetails
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField
from wtforms.validators import InputRequired
import io
import base64
import matplotlib as plt


class MoneyDetails(FlaskForm):
    amount=IntegerField('Amount', validators=[InputRequired('Amount cannot be empty')])
    type=RadioField('Type', choices=[('expenditure','Expenditure'), ('income','Income')])
    category=StringField('Category')
    submit=SubmitField('Add')

fin_bp=Blueprint(__name__, 'fin')

@fin_bp.route('/view_fin')
def view_fin():
    if 'user' not in session:
        return redirect(url_for('login.signup'))
    details=FinDetails.query.all()
    return render_template('view_fin.html', details=details)

@fin_bp.route('/add_fin', methods=['GET', 'POST'])
def add_fin():
    if 'user' not in session:
        return redirect(url_for('login.signup'))
    form=MoneyDetails()
    if form.validate_on_submit():
        amount=form.amount.data
        type=form.type.data
        category=form.category.data
        new_fin=FinDetails(amount=amount, type=type, category=category)
        db.session.add(new_fin)
        db.session.commit()
        flash("Your details have been added successfully!", 'success')
    return redirect(url_for('fin.view_fin'))

@fin_bp.route('/view_chart')
def view_chart():
    if 'user' not in session:
        return redirect(url_for('login.signup'))
    data=FinDetails.query.with_entities(FinDetails.amount, FinDetails.category).filter_by(category='expenditure').all()
    amount=[x[0] for x in data]
    category=[x[1] for x in data]

    plt.pie(amount, label=category)
    plt.title("Spending distribution")

    pie_buf=io.BytesIO()
    plt.savefig(pie_buf, format='png')
    pie_buf.seek(0)
    pie_img=base64.b64encode(pie_buf.getvalue()).decode('utf-8')
    pie_buf.close()
    plt.close()

    data2=FinDetails.query.with_entities(FinDetails.amount, FinDetails.category).filter_by(category='income').all()
    amount2=[x[0] for x in data]
    category2=[x[1] for x in data]

    plt.pie(amount, label=category)
    plt.title("Earning distribution")

    pie_buf2=io.BytesIO()
    plt.savefig(pie_buf2, format='png')
    pie_buf2.seek(0)
    pie_img2=base64.b64encode(pie_buf2.getvalue()).decode('utf-8')
    pie_buf2.close()
    plt.close()

    return render_template(charts.html, pie_img=pie_img, pie_img2=pie_img2)




    