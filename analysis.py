from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView


analysis = Blueprint('analysis', __name__, template_folder='templates')


class TrafficInquiry(MethodView):
    # 话务数据分布显示/查询  faafhalks

    def get(self):
        return render_template('inquiry/station.html')


class TrafficAnalysis(MethodView):
    # 话务分析

    def get(self):
        return render_template('inquiry/community.html')


analysis.add_url_rule('/analysis/inquiry', view_func=TrafficInquiry.as_view('inquiry'))
analysis.add_url_rule('/analysis/analysis', view_func=TrafficAnalysis.as_view('analysis'))
