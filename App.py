from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/",methods=['POST','GET'])
def hello_world():
    print("printing to console")
    return "<p>Hello, World!</p>",200