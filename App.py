from flask import Flask,request
from flask_cors import CORS
import os
from flask import send_from_directory

app = Flask(__name__)
CORS(app)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/test",methods=['POST'])
def hello_world():
    content =  request.get_data()
    print(content)
    return "Hello, World!",200


if __name__ == '__main__':
  print('\nstarting...')
  app.run(debug=True)