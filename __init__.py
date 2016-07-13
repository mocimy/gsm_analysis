from functools import wraps
from flask import Flask, session, request, redirect, url_for
from flask_psycopg2 import Psycopg2

app = Flask(__name__)
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = '123456'
app.config['PSYCOPG2_DATABASE_URI'] = 'pgsql://postgres:@localhost/gsm'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


psycopg2 = Psycopg2(app)


def register_blueprints(app):
    from gsm_analysis.login import login
    from gsm_analysis.data import data
    from gsm_analysis.inquiry import inquiry
    from gsm_analysis.traffic import traffic
    from gsm_analysis.neighbor import neighbor
    app.register_blueprint(login)
    app.register_blueprint(data)
    app.register_blueprint(inquiry)
    app.register_blueprint(traffic)
    app.register_blueprint(neighbor)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

register_blueprints(app)

if __name__ == '__main__':
    app.run()
