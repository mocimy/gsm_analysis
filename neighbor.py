from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from gsm_analysis import psycopg2


neighbor = Blueprint('neighbor', __name__, template_folder='templates')


class CalcView(MethodView):
    # 邻区计算
    def get(self):
        if 'distance' in request.args:
            cur = psycopg2.connect().cursor()
            cur.execute("select distanceCalculate(%s)", (float(request.args['distance']),))
            return jsonify(success=True)
        return render_template('neighbor/calc.html')


class InquiryView(MethodView):
    # 邻区查询

    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "CellID" from area_infor''')
        data = [x[0] for x in cur.fetchall()]
        if 'cell_id' in request.args:
            cur.execute("select * from displayDistance(%s)", (request.args['cell_id'],))
            data = cur.fetchone()
            res = '<br>'.join([x[1]+",距离:"+x[6] for x in data])
            return jsonify(res=res)
        return render_template('neighbor/inquiry.html', names=data)


neighbor.add_url_rule('/neighbor/calc', view_func=CalcView.as_view('calc'))
neighbor.add_url_rule('/neighbor/inquiry', view_func=InquiryView.as_view('inquiry'))
