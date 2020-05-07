import os
import werkzeug
from werkzeug.utils import secure_filename

from flask import Flask, request, make_response, jsonify, render_template

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getcwd()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/select")
def select():
    return render_template('select.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
       return render_template('upload.html')
    if request.method == 'POST':
       file = request.files['uploadFile']
       if file:
          filename = secure_filename(file.filename)
          filepath = os.path.join(UPLOAD_DIR, filename) 
          file.save(filepath)
          ### データベースインサートクラスに渡す
          with open(filepath, "r") as test_data:
               content = test_data.read()

          os.remove(filepath)
          return render_template('select.html',content=content)
    

 
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