from functools import wraps
from flask import Blueprint, request, redirect, render_template, url_for, session
from flask.views import MethodView
from gsm_analysis import app


login = Blueprint('login', __name__, template_folder='templates')


class LoginView(MethodView):
    # 登陆界面

    def get(self):
        if 'username' in session:
            return redirect(url_for('data.data'))
        return render_template('login.html')

    def post(self):
        if 'username' in request.form and 'password' in request.form:
            if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
                session['username'] = request.form['username']
                return redirect(url_for('data.data'))
        return render_template('login.html', fail=True)


class LoginOutView(MethodView):

    def get(self):
        session.pop('username', None)
        return redirect(url_for('login.login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login.login'))
        return f(*args, **kwargs)
    return decorated_function


login.add_url_rule('/', view_func=LoginView.as_view('login'))
login.add_url_rule('/login_out', view_func=LoginOutView.as_view('login_out'))
