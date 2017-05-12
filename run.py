# -*- coding: utf-8 -*-
import os
import re
import json
import random
import urllib
import datetime
from main.form import BlogForms
from flask import Flask, request, render_template, url_for, make_response

app = Flask(__name__, static_url_path='')
app.secret_key = 'fdsjdsafjlkfdsajlk'
app.debug = True


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (filename_prefix, str(random.randrange(1000, 10000)))


@app.route('/')
def index():
    form = BlogForms()
    return render_template('index.html', form=form)


@app.route('/blog-form/', methods=['POST'])
def blog_form():
    """接收提交过来表单数据"""
    form = BlogForms(request.form)
    form = form.body.data
    return form


@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """CKEditor file upload
        文件上传，
    """
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)

        # rnd_name = '%s%s' % (gen_rnd_filename(), fext)   # python2 老代码
        rnd_name = '{}{}'.format(gen_rnd_filename(), fext)

        filepath = os.path.join(app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            # url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
            url = url_for('static', filename='{}/{}'.format('upload', rnd_name))
    else:
        error = 'post error'
    res = """<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response


if __name__ == '__main__':
    app.run()
