#import library
import pandas as pd
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request,jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import gevent.pywsgi
import joblib
from flask_jwt_extended import (JWTManager,jwt_required,
                                create_access_token,get_jwt_identity)

#import module
import models
from resources.messages import messages_api
from resources.users import users_api
from resources.mentals import mentals_api


#inisiasi object flask
app = Flask(__name__)
#inisiasi object flask_cors
CORS(app, support_credentials=True)
#ACCESS_TOKEN_JWT
app.config['SECRET_KEY'] ='scfsdsdfsdfsferwer'
app.config['JWT_BLACKLIST_ENABLED'] =True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] =['access,refresh']
jwt=JWTManager(app)

app.register_blueprint(messages_api,url_prefix='/api/v1')
app.register_blueprint(users_api,url_prefix='/api/v1')
app.register_blueprint(mentals_api,url_prefix='/api/v1')


#logout
blacklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti=decrypted_token['jti']
    return jti in blacklist

@app.route('/api/v1/user/logout')
def logout():
    return {'msg':'berhasil logout'}
# api = Api(app)

# users = {}

# class User(Resource):
#     def get(self,user_id):
#         return {'nama':users[user_id]}

#     def put(self, user_id):
#         users[user_id] = request.form['user']
#         return {'nama': users[user_id]}

# api.add_resource(messages.MessageList, '/messages')


if __name__ == '__main__':
    models.initialize()   
    # Untuk mode pengembangan
    # app.run(debug=True)

    # Gunakan wsgi server untuk deployment (production)
    http_server = gevent.pywsgi.WSGIServer(("127.0.0.1", 80), app)
    http_server.serve_forever()
