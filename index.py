from flask import Flask, render_template, request, send_from_directory, after_this_request
from werkzeug.utils import secure_filename
import os, time, hashlib

from picen import picen

app = Flask(__name__)
HEADER = 'picrc_'

@app.route('/', methods=['GET'])
def home():
   return render_template('result.html')

@app.route('/', methods=['POST'])
def enpost():
    ifile = request.files.get('file')
    psswd = request.form['password']
    psswd = psswd if psswd else "123456"
    if not ifile:
        return 'invalid'

    td = str(time.time())
    m = hashlib.md5()
    m.update((td + request.remote_addr).encode())

    rdnid = m.hexdigest()
    iname = secure_filename(ifile.filename)
    sufix = os.path.splitext(iname)[-1]
    # sufix = '.picrc'

    sname = rdnid + '_' + iname
    oname = HEADER + rdnid + sufix

    ifile.save(sname)
    picen(psswd, sname, oname)
    os.remove(sname)

    @after_this_request
    def delf(res):
        if os.path.exists(oname):
            os.remove(oname)
        return res

    return send_from_directory('', oname, as_attachment=True)

if __name__ == "__main__":
    app.run()