from datetime import datetime as dt
import json
import os
import pathlib
#import re
import sys
import werkzeug
from werkzeug.utils import secure_filename

from flask import Flask, request, make_response, jsonify, render_template

currentdir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(currentdir)+"/../models/")
from tablestorage import TableStorageOperate

#sys.path.append(str(currentdir)+"/../")
#import models

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getcwd()
tablename = 'testsample'


@app.route("/")
def hello():
    return "Hello World"

@app.route("/select", methods=['GET', 'POST'])
def select():
    if request.method == 'GET':
       return render_template('select.html')
    if request.method == 'POST':
       pkey = request.form.get('partitionkey')
       rkey = request.form.get('rowkey')
       if len(pkey) !=0 and len(rkey) !=0:
          conditions = [pkey,rkey]
       elif len(pkey):
          conditions = "PartitionKey eq '" + pkey +"'"
       else:
          conditions = ""
       # Call Select Records
       ts = TableStorageOperate()
       results = ts.select_records(conditions,tablename)

       # Get Title
       keys = []
       for i,rs in enumerate(results):
           if type(rs) is str:
              rs = dict(rs)
           if i == 0:
              keys = [ k for k in rs.keys()]
           else:
              break
       # render html
       body = """
       <div id = content>
       <style type="text/css">
            th, td {
                    width: 100px ;
            }
            thead, tbody {
            display: block;
            }
            tbody {
            overflow-x: hidden;
            overflow-y: scroll;
            height: 600px;
            }
       </style>
       <table border=1>
            <thead>
                <tr>
       """
       for k in keys:
           if k != 'etag':
              body += '<th>' + k + '</th>'
       body += '</tr></thead>'

       body += '<tbody>'
       for r in results:
           body += '<tr>'
           for k in keys:
               if k != 'etag':
                  if type(r[k]) is str:
                     body += '<td>' + r[k] + '</td>'
                  elif isinstance(r[k],dt):
                     v = r[k].strftime('%Y-%m-%d %H:%M:%S')
                     body += '<td>' + v + '</td>'
                  else:
                     body += '<td>－</td>'
           body += '</tr>'
       body += """
            </tbody>
        </table>
        </div>
        """   
       return render_template('select.html',content=body)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
       return render_template('upload.html',content='')
    if request.method == 'POST':
       file = request.files['uploadFile']
       if file:
          filename = secure_filename(file.filename)
          filepath = os.path.join(UPLOAD_DIR, filename) 
          file.save(filepath)
          # Call Table Insert 
          # ToDo Filename get set Tablename
          ts = TableStorageOperate()
          ts.insert_table(filepath,tablename)
          os.remove(filepath)
          return render_template('upload.html',content='アップロード完了しました')

 
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    title = str(error.code) + 'エラー' 
    content = str(error.name)
    description = str(error.description)
    return render_template('error.html',title=title,content=content,description=description)

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    title = 'ファイルエラー'
    content = "werkzeug.exceptions.RequestEntityTooLarge"
    description = 'result : file size is overed.'
    return render_template('error.html',title=title,content=content,description=description)

if __name__ == '__main__':
    app.run(debug=True)