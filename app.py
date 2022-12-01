#import library
import pandas as pd
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS,cross_origin
import gevent.pywsgi
from flask_jwt_extended import (JWTManager,jwt_required,get_jwt,get_jwt_identity,
                                create_access_token,set_access_cookies,unset_jwt_cookies)
from datetime import datetime,timedelta,timezone
#import module
import models
from resources.messages import messages_api
from resources.users import users_api
from resources.mentals import mentals_api


#inisiasi object flask
app = Flask(__name__)
#inisiasi object flask_cors
# cors_config = {
#     'origins':'*',
#     'methods':['GET','POST'],
#     'allow-headers':'*'
# }
# CORS(app,resources={r"/api/v1/*":cors_config})
CORS(app,allow_headers=['Content-Type'])
#ACCESS_TOKEN_JWT
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in your code!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt=JWTManager(app)

app.register_blueprint(messages_api,url_prefix='/api/v1')
app.register_blueprint(users_api,url_prefix='/api/v1')
app.register_blueprint(mentals_api,url_prefix='/api/v1')


if __name__ == '__main__':
    models.initialize()   
    # Untuk mode pengembangan
    app.run(debug=True,host='0.0.0.0', port=80)
    # Gunakan wsgi server untuk deployment (production)
    # http_server = gevent.pywsgi.WSGIServer(("127.0.0.1", 80), app)
    # http_server.serve_forever()
