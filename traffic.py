from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from gsm_analysis import psycopg2


traffic = Blueprint('traffic', __name__, template_folder='templates')


class MinuteTrafficView(MethodView):
    # 分钟级话务量查询
    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "CellID" from area_infor''')
        data = [x[0] for x in cur.fetchall()]
        return render_template('traffic/minute.html', names=data)

    def post(self):
        if 'cell_id' in request.form and 'date' in request.form and 'begin_time' in request.form and 'end_time' in request.form:
            cell_id = request.form['cell_id']
            date = request.form['date'][3:].replace('-', '')
            begin_time = int(request.form['begin_time'].replace(':', ''))
            end_time = int(request.form['end_time'].replace(':', ''))
            cur = psycopg2.connect().cursor()
            if request.form['is_fifteen'] == 'true':
                time = (begin_time % 100 - end_time % 100) % 15
                if end_time % 100 - time > 0:
                    end_time -= time
                else:
                    end_time -= 100
                    end_time += (60-time)

                cur.execute("select * from get15MinuteTraffic(%s,%s,%s,%s)", (cell_id, date, begin_time, end_time))
            else:
                cur.execute("select * from getMinuteTraffic(%s,%s,%s,%s)", (cell_id, date, begin_time, end_time))
            data = cur.fetchall()
            print(data)
            return jsonify(time=[x[0] for x in data],
                           traffavg=[x[1] for x in data],
                           callcongs=[x[2] for x in data],
                           rate=[x[3] for x in data],
                           traffline=[x[4] for x in data])


class CongsAreaView(MethodView):
    # 拥塞小区查询

    def get(self):
        return render_template('traffic/congs.html')

    def post(self):
        if 'rate' in request.form and 'date' in request.form and 'begin_time' in request.form and 'end_time' in request.form:
            date = request.form['date'][3:].replace('-', '')
            begin_time = int(request.form['begin_time'][:2])
            end_time = int(request.form['end_time'][:2])
            cur = psycopg2.connect().cursor()
            cur.execute("select * from getCongsAreaInfor(%s, %s, %s, %s)", (float(request.form['rate']), date, begin_time, end_time ))
            data = cur.fetchall()
            result = ""
            for x in data:
                result += "小区:"+str(x[0])+"<br>小时级话务量:"+str(x[9])+"<br>小时级拥塞率:" + str(x[10]) + "<br>小时级半速率话务量比例:" + str(x[11]) + "<br>小时级每线话务量:" + str(x[12]) + "<br><br>"
            return jsonify(res=result)
        return jsonify(success=False)

class TrafficAnalysis(MethodView):
    # 话务分析

    def get(self):
        conn = psycopg2.connect()
        cur = conn.cursor()
        cur.execute("select trafficAnalyze()")
        cur.fetchone()
        conn.commit()

        return render_template('traffic/analysis.html')


traffic.add_url_rule('/traffic/inquiry', view_func=MinuteTrafficView.as_view('minute'))
traffic.add_url_rule('/traffic/congs', view_func=CongsAreaView.as_view('congs'))
traffic.add_url_rule('/traffic/analysis', view_func=TrafficAnalysis.as_view('analysis'))
