from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView


data = Blueprint('data', __name__, template_folder='templates')


class DataManage(MethodView):

    def get(self):
        return render_template('data.html')


data.add_url_rule('/data/', view_func=DataManage.as_view('data'))
