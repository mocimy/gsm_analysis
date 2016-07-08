import os
from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from werkzeug.utils import secure_filename


data = Blueprint('data', __name__, template_folder='templates')


class DataManage(MethodView):

    def get(self):
        return render_template('data.html')


class ImportView(MethodView):

    def post(self):
        if 'attachmentName' in request.files:
            file = request.files['attachmentName']
            if file:
                filename = secure_filename(file.name)
                file.save(os.path.join(os.path.dirname(__file__), filename))
                return '上传成功'
        return '上传失败'

data.add_url_rule('/', view_func=DataManage.as_view('data'))
data.add_url_rule('/data/import', view_func=ImportView.as_view('import'))
