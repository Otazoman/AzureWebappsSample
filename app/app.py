#from datetime import datetime as dt
#import json
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

sys.path.append(str(currentdir)+"/../controllers/")
from viewrender import TableRender

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getcwd()
tablename = 'testsample'


@app.route("/")
def hello():
    return "Hello Sample"

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
       vr = TableRender()
       body = vr.tablerender(results)
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

@app.route("/dalete", methods=['GET', 'POST'])
def dalete():
    ts = TableStorageOperate()
    vr = TableRender()
    if request.method == 'GET':
       conditions = ""
       results = ts.select_records(conditions,tablename)
       body = vr.tablerender(results)
       return render_template('dalete.html',content=body)
    if request.method == 'POST':
       pkey = request.form.get('partitionkey')
       rkey = request.form.get('rowkey')
       if len(pkey) !=0 and len(rkey) !=0:
          conditions = [pkey,rkey]
       elif len(pkey):
          conditions = "PartitionKey eq '" + pkey +"'"
       else:
          conditions = ""
       # Call Delete Records
       ts.delete_records(conditions,tablename)
       # After view Render
       conditions = ""
       results = ts.select_records(conditions,tablename)
       body = vr.tablerender(results)
       return render_template('dalete.html',content=body)



 
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