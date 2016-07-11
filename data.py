import os
import xlrd
from io import StringIO, BytesIO
from flask import Blueprint, request, redirect, render_template, url_for, send_file
from flask.views import MethodView
from werkzeug.utils import secure_filename
from gsm_analysis import psycopg2


data = Blueprint('data', __name__, template_folder='templates')
table = {
    'MS信息': 'ms_infor',
    'MSC信息': 'msc_infor',
    'BSC信息': 'bsc_infor',
    'BTS信息': 'bts_infor',
    '小区基本信息': 'area_infor',
    '小区频点表': 'area_freq',
    '天线信息': 'aerial_infor',
    '邻区信息': 'neighbor_infor',
    '20个小区一周分钟级话务数据': 'tele_traffic',
    '路测信息': 'road_test'
}


class DataManage(MethodView):

    def get(self):
        return render_template('data.html')


class ImportView(MethodView):

    def post(self):
        if 'attachmentName' in request.files:
            file = request.files['attachmentName']
            if file:
                filename = secure_filename(file.name)
                file.save(filename)
                book = xlrd.open_workbook(filename)
                conn = psycopg2.connect()
                cur = conn.cursor()

                input_buffer = StringIO()
                n = 0
                for sh in book.sheets():
                    for i in range(2, sh.nrows):
                        input_buffer.write('\t'.join([str(x) for x in sh.row_values(i)])+'\n')
                        if n % 50 == 0:
                            input_buffer.seek(0)
                            cur.copy_from(input_buffer, table[sh.name])
                            conn.commit()
                            input_buffer = StringIO()
                        n += 1
                    cur.copy_from(input_buffer, table[sh.name])
                    input_buffer = StringIO()
                    conn.commit()
                cur.execute("select * from ms_infor")
                print(cur.fetchall())
                return '导入成功'
        return '导入失败'


class ExportView(MethodView):

    def get(self, tname):
        conn = psycopg2.connect()
        cur = conn.cursor()
        file = BytesIO()
        cur.copy_to(file, tname)
        file.seek(0)
        return send_file(file,
                         attachment_filename=tname+".txt",
                         as_attachment=True,
                         mimetype='text/csv')

data.add_url_rule('/data', view_func=DataManage.as_view('data'))
data.add_url_rule('/data/import', view_func=ImportView.as_view('import'))
data.add_url_rule('/data/export/<tname>', view_func=ExportView.as_view('export'))
