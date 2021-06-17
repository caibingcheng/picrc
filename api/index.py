# coding=utf-8

from flask import Flask, render_template, request, send_from_directory, after_this_request, Response, stream_with_context, make_response
from werkzeug.utils import secure_filename
import mimetypes
import os
import sys
import time
import hashlib
import stat

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)
from utils.picen import picen


app = Flask(__name__, static_folder="../static",
            template_folder="../templates")
HEADER = 'picrc_'

@app.route('/', methods=['GET'])
def home():
    return render_template('result.html')


@app.route('/', methods=['POST'])
def enpost():
    ifile = request.files.get('file')
    if not ifile:
        return render_template('result.html')
    psswd = request.form['password']
    psswd = psswd if psswd else "123456"

    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())

    rdnid = m.hexdigest()
    iname = secure_filename(ifile.filename)
    sufix = os.path.splitext(iname)[-1]
    oname = HEADER + rdnid + sufix

    file_content = ifile.read()
    dst = picen(psswd, file_content)

    response = make_response(dst)
    response.headers['Content-Type'] = mimetypes.guess_type(iname)[0]
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(oname)
    response.headers['content-length'] = len(dst)
    return response

if __name__ == "__main__":
    app.run()
