from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView
from gsm_analysis import psycopg2
from gsm_analysis.login import login_required


neighbor = Blueprint('neighbor', __name__, template_folder='templates')


class CalcView(MethodView):
    # 邻区计算
    @login_required
    def get(self):
        return render_template('neighbor/calc.html')

    @login_required
    def post(self):
        if 'distance' in request.form:
            conn = psycopg2.connect()
            cur = conn.cursor()
            cur.execute("select distanceCalculate(%s)", (float(request.form['distance']),))
            cur.fetchall()
            conn.commit()
            return jsonify(success=True)
        return jsonify(success=False)


class InquiryView(MethodView):
    # 邻区查询

    @login_required
    def get(self):
        cur = psycopg2.connect().cursor()
        cur.execute('''select "CellID" from area_infor''')
        data = [x[0] for x in cur.fetchall()]
        if 'cell_id' in request.args:
            cur.execute("select * from displayDistance(%s)", (request.args['cell_id'],))
            data = cur.fetchall()
            res = '<br>'.join([x[1]+",距离:"+str(x[6]) for x in data])
            return jsonify(res=res)
        return render_template('neighbor/inquiry.html', names=data)


neighbor.add_url_rule('/neighbor/calc', view_func=CalcView.as_view('calc'))
neighbor.add_url_rule('/neighbor/inquiry', view_func=InquiryView.as_view('inquiry'))
