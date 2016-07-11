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


login.add_url_rule('/', view_func=LoginView.as_view('login'))
