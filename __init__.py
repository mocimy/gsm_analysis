from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19950301@localhost/database'
db = SQLAlchemy(app)


def register_blueprints(app):
    from gsm_analysis.data import data
    from gsm_analysis.inquiry import inquiry
    from gsm_analysis.analysis import analysis
    from gsm_analysis.neighbour import neighbour
    app.register_blueprint(data)
    app.register_blueprint(inquiry)
    app.register_blueprint(analysis)
    app.register_blueprint(neighbour)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
