from flask import flash, Blueprint, render_template, redirect, url_for, session
from app import db
from app.models import FinDetails
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, IntegerField
from wtforms.validators import InputRequired
import io
import base64
import matplotlib
import matplotlib.pyplot as plt
from sqlalchemy import func
matplotlib.use('Agg')


class MoneyDetails(FlaskForm):
    amount=IntegerField('Amount', validators=[InputRequired('Amount cannot be empty')])
    type=RadioField('Type', choices=[('expenditure','Expenditure'), ('income','Income')])
    category=StringField('Category')
    submit=SubmitField('Add')

fin_bp=Blueprint('fin', __name__)

@fin_bp.route('/view_fin', methods=['GET', 'POST'])
def view_fin():
    if 'user' not in session:
        return redirect(url_for('login.signup'))

    form=MoneyDetails()
    if form.validate_on_submit():
        amount=form.amount.data
        type=form.type.data
        category=form.category.data
        new_fin=FinDetails(amount=amount, type=type, category=category, user_id=session['user'])
        db.session.add(new_fin)
        db.session.commit()
        flash("Your details have been added successfully!", 'success')
    details=FinDetails.query.filter_by(user_id=session['user']).all()
    return render_template('view_fin.html', details=details, form=form)

@fin_bp.route('/view_chart')
def view_chart():
    if 'user' not in session:
        return redirect(url_for('login.signup'))
    data=FinDetails.query.with_entities(func.sum(FinDetails.amount), FinDetails.category).filter_by(type='expenditure', user_id=session['user']).group_by(FinDetails.category).all()
    amount=[x[0] for x in data]
    category=[x[1] for x in data]

    plt.pie(amount, labels=category, autopct="%1.1f%%")
    plt.title("Spending distribution")

    pie_buf=io.BytesIO()
    plt.savefig(pie_buf, format='png')
    pie_buf.seek(0)
    pie_img=base64.b64encode(pie_buf.getvalue()).decode('utf-8')
    pie_buf.close()
    plt.close()

    data2=FinDetails.query.with_entities(func.sum(FinDetails.amount), FinDetails.category).filter_by(type='income', user_id=session['user']).group_by(FinDetails.category).all()
    amount2=[x[0] for x in data2]
    category2=[x[1] for x in data2]

    plt.pie(amount2, labels=category2, autopct="%1.1f%%")
    plt.title("Earning distribution")

    pie_buf2=io.BytesIO()
    plt.savefig(pie_buf2, format='png')
    pie_buf2.seek(0)
    pie_img2=base64.b64encode(pie_buf2.getvalue()).decode('utf-8')
    pie_buf2.close()
    plt.close()

    return render_template('charts.html', pie_img=pie_img, pie_img2=pie_img2)




    