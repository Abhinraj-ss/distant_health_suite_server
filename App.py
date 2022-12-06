from flask import Flask
from flask_cors import CORS
import os
from flask import send_from_directory

app = Flask(__name__)
CORS(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                               
@app.route("/",methods=['POST','GET'])
def hello_world():
    print("printing to console")
    return "<p>Hello, World!</p>",200