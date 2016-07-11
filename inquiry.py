from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from gsm_analysis import psycopg2


inquiry = Blueprint('inquiry', __name__, template_folder='templates')


class StationInfo(MethodView):
    # 基站信息查询

    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "BtsName" from bts_infor''')
        data = [x[0] for x in cur.fetchall()]
        if 'bts_name' in request.args:
            print(request.args['bts_name'])
            cur.execute("select * from getBtsByName(%s)", (request.args['bts_name'],))
            data = cur.fetchone()
            res = '<br>'.join([cur.description[i][0] + ':' + str(data[i]) for i in range(len(cur.description))])
            return jsonify(res=res)
        return render_template('inquiry/bts.html', names=data)


class CommunityInfo(MethodView):
    # 小区信息查询

    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "CellID" from area_infor''')
        data = [x[0] for x in cur.fetchall()]
        if 'cell_id' in request.args:
            cur.execute("select * from getAreaInfoById(%s)", (request.args['cell_id'],))
            data = cur.fetchone()
            res = '<br>'.join([cur.description[i][0] + ':' + str(data[i]) for i in range(len(cur.description))])
            cur.execute("select * from  getAreaMaxFreqById(%s)", (request.args['cell_id'],))
            data = cur.fetchone()
            res += "<br>最大载频配置:"+str(data[0])
            return jsonify(res=res)
        return render_template('inquiry/area.html', names=data)


class TrafficInfo(MethodView):
    # 话务统计信息查询

    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "CellID" from area_infor''')
        data = [x[0] for x in cur.fetchall()]
        return render_template('inquiry/traffic.html', names=data)

    def post(self):
        if 'cell_id' in request.form and 'date' in request.form and 'begin_time' in request.form and 'end_time' in request.form:
            cell_id = request.form['cell_id']
            date = request.form['date'][3:].replace('-','')
            begin_time = int(request.form['begin_time'][:2])
            end_time = int(request.form['end_time'][:2])
            cur = psycopg2.connect().cursor()
            cur.execute("select * from getHourlyTraffic(%s,%s,%s,%s)", (cell_id, date, begin_time, end_time))
            data = cur.fetchall()
            print(data)
            return jsonify(time=[x[0] for x in data],
                           traffavg=[x[1] for x in data],
                           callcongs=[x[2] for x in data],
                           rate=[x[3] for x in data],
                           traffline=[x[4] for x in data])


inquiry.add_url_rule('/inquiry/station_info', view_func=StationInfo.as_view('bts'))
inquiry.add_url_rule('/inquiry/community_info', view_func=CommunityInfo.as_view('area'))
inquiry.add_url_rule('/inquiry/traffic_info', view_func=TrafficInfo.as_view('traffic'))
