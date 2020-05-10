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
from viewrender import HtmlRender

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getcwd()
ts = TableStorageOperate()
vr = HtmlRender()

@app.route("/")
def started():
    return render_template('index.html')

@app.route("/select", methods=['GET', 'POST'])
def select():
    #Get Tablelist
    tl = ts.get_table_list()
    default_val = ts.get_default_table(tl)
    if request.method == 'GET':
       slbox = vr.make_selectbox(tl,default_val)
       return render_template('select.html',selectbox=slbox)
    if request.method == 'POST':
       tn = request.form.get('table_name')
       pkey = request.form.get('partitionkey')
       rkey = request.form.get('rowkey')
       if len(pkey) !=0 and len(rkey) !=0:
          conditions = [pkey,rkey]
       elif len(pkey):
          conditions = "PartitionKey eq '" + pkey +"'"
       else:
          conditions = ""

       if request.form.get('search') == '検索':
          # Call Select Records
          results = ts.select_records(conditions,tn)
          body = vr.tablerender(results)
          slbox = vr.make_selectbox(tl,tn)
          return render_template('select.html',content=body,selectbox=slbox)
       elif request.form.get('delete') == '削除':
          # Call Delete Records
          ts.delete_records(conditions,tn)
          ac = ""
          results = ts.select_records(ac,tn)
          body = vr.tablerender(results)
          slbox = vr.make_selectbox(tl,tn)
          return render_template('select.html',content=body,selectbox=slbox)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
       return render_template('upload.html',content='')
    if request.method == 'POST':
       #tn = request.form.get('table_name')
       file = request.files['uploadFile']
       if file:
          filename = secure_filename(file.filename)
          # Get Upsert TableName
          tn = os.path.splitext(filename)[0]
          filepath = os.path.join(UPLOAD_DIR, filename) 
          file.save(filepath)
          # Call Table Insert 
          ts = TableStorageOperate()
          ts.insert_table(filepath,tn)
          os.remove(filepath)
          return render_template('upload.html',content='アップロード完了しました')

"""
@app.route("/delete", methods=['GET', 'POST'])
def delete():
    #Get Tablelist
    tl = ts.get_table_list()
    default_val = ts.get_default_table(tl)
    if request.method == 'GET':
       slbox = vr.make_selectbox(tl,default_val)
       conditions = ""
       results = ts.select_records(conditions,default_val)
       body = vr.tablerender(results)
       return render_template('delete.html',content=body,selectbox=slbox)
    if request.method == 'POST':
       tn = request.form.get('table_name')
       pkey = request.form.get('partitionkey')
       rkey = request.form.get('rowkey')
       if len(pkey) !=0 and len(rkey) !=0:
          conditions = [pkey,rkey]
       elif len(pkey):
          conditions = "PartitionKey eq '" + pkey +"'"
       else:
          conditions = ""
       # Call Delete Records
       ts.delete_records(conditions,tn)
       # After view Render
       conditions = ""
       results = ts.select_records(conditions,tn)
       body = vr.tablerender(results)
       slbox = vr.make_selectbox(tl,tn)
       return render_template('delete.html',content=body,selectbox=slbox)
"""

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