import os  #app 
import models
import requests
from flask import Flask, request, jsonify, g
from flask_login import LoginManager
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict
from resources.users import user
from resources.medicines import medicine

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.secret_key = 'help meee'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/search/<brand_name>', methods=['GET'])
def index(brand_name):
    fda_label_key = 'Pb5Vody5Yg2QRlYWBCJ0DNzO1OR3DX2JbgtANafr'
    fda_label_url = 'https://api.fda.gov/drug/label.json?api_key={}&limit=100'.format(fda_label_key)
    response = fda_label_url + '&search=openfda.brand_name:{}'.format(brand_name)
    fda_label_request = requests.get(response)
    # print('label_request.json: {}'.format(fda_label_request.json()))
    return jsonify(fda_label_request.json())



CORS(user, origins=['http://localhost:3000', 'https://capstone-react.herokuapp.com'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/users')

CORS(medicine, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(medicine, url_prefix='/api/v1/medicines')

CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

if 'ON_HEROKU' in os.environ:
    print('Hitting')
    models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)