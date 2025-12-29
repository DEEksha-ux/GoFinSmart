from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)

    app.config['SECRET_KEY']='super-secret'
    app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:mypass@localhost/gofinsmart_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)

    from app.models import UserDetails, FinDetails

    with app.app_context():
        db.create_all()

    from app.routes.home import login_bp
    from app.routes.finance import fin_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(fin_bp)
    print(app.root_path)

    
    return app



