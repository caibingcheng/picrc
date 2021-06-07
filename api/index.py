# coding=utf-8

from flask import Flask, render_template, request, send_from_directory, after_this_request
from werkzeug.utils import secure_filename
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

os.chmod("./", stat.S_IRWXO | stat.S_IRWXG | stat.S_IRWXU)

@app.route('/', methods=['GET'])
def home():
    return render_template('result.html')


@app.route('/', methods=['POST'])
def enpost():
    print('picrc post in', 'file' in request.files)
    ifile = request.files.get('file')
    if not ifile:
        return render_template('result.html')
    psswd = request.form['password']
    psswd = psswd if psswd else "123456"
    print('picrc post params')

    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())
    print('picrc hash prefix')

    rdnid = m.hexdigest()
    iname = secure_filename(ifile.filename)
    sufix = os.path.splitext(iname)[-1]
    # sufix = '.picrc'

    sname = rdnid + '_' + iname
    oname = HEADER + rdnid + sufix
    print('picrc gen name')

    ifile.save(sname)
    print('picrc save', sname)
    picen(psswd, sname, oname)
    print('picrc process', sname)
    os.remove(sname)
    print('picrc remove', sname)

    @after_this_request
    def delf(res):
        print('picrc remove', oname)
        if os.path.exists(oname):
            os.remove(oname)
        return res

    return send_from_directory('../', oname, as_attachment=True)


if __name__ == "__main__":
    app.run()
