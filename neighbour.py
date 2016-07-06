from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView


neighbour = Blueprint('neighbour', __name__, template_folder='templates')


class NeighbourCalc(MethodView):
    # 邻区计算

    def get(self):
        return render_template('inquiry/station.html')


class NeighbourInquiry(MethodView):
    # 邻区查询

    def get(self):
        return render_template('inquiry/community.html')


neighbour.add_url_rule('/neighbour/calc', view_func=NeighbourCalc.as_view('calc'))
neighbour.add_url_rule('/neighbour/inquiry', view_func=NeighbourInquiry.as_view('inquiry'))