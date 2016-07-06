from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView


inquiry = Blueprint('inquiry', __name__, template_folder='templates')


class StationInfo(MethodView):
    # 基站信息查询

    def get(self):
        return render_template('inquiry/station.html')


class CommunityInfo(MethodView):
    # 小区信息查询

    def get(self):
        return render_template('inquiry/community.html')


class TrafficInfo(MethodView):
    # 话务统计信息查询

    def get(self):
        return render_template('inquiry/traffic.html')


inquiry.add_url_rule('/inquiry/station_info', view_func=StationInfo.as_view('station'))
inquiry.add_url_rule('/inquiry/community_info', view_func=CommunityInfo.as_view('community'))
inquiry.add_url_rule('/inquiry/traffic_info', view_func=TrafficInfo.as_view('traffic'))
