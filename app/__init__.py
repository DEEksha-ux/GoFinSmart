from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY']='super-secret'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:mypass@localhost/GoFinSmart_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.__init__(app)

    from app.routes.home import login_bp
    from app.routes.finance import fin_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(fin_bp)

    return app
