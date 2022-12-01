from flask import jsonify, Blueprint, abort,make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
from hashlib import md5
import json
import models
from flask_jwt_extended import (JWTManager,jwt_required,get_jwt,get_jwt_identity,
                                create_access_token,set_access_cookies,unset_jwt_cookies,create_refresh_token)
from datetime import datetime,timedelta,timezone

user_fields = {
    'username': fields.String,
    'access_token': fields.String
}

class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='username wajib ada',
            location=['form', 'args'],

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password wajib ada',
            location=['form', 'args'],

        )
        super().__init__()


class UserReg(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            models.User.select().where(models.User.username == username).get()
        except models.User.DoesNotExist:
            # daftarun usernya
            user = models.User.create(
                username=username,
                password=md5(password.encode('utf-8')).hexdigest()
            )
            additional_claims = {"aud": "some_audience", "foo": "bar"}
            access_token = create_access_token(username, additional_claims=additional_claims)
            return jsonify(access_token=access_token)
        else:
            raise Exception('username sudah terdaftar')
 
    @jwt_required()
    def get(self):
        claims = get_jwt()
        return jsonify(foo=claims["foo"])


class User(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        username = args.get('username')
        password = args.get('password')
        try:
            hashpassword = md5(password.encode('utf-8')).hexdigest()
            username = models.User.get((models.User.username == username) & (
                models.User.password == hashpassword))
        except models.User.DoesNotExist:
            return {'message': 'user or passsword is wrong'}
        else:
            username = args.get('username')
            # access_token = create_access_token(identity=username)
            # return make_response(jsonify({'message': 'selamat login','token':access_token}),200)
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)
            info='access token bertahan 1 jam dan refresh token bertahan 30 hari'
            return jsonify({'info':info,'access_token':access_token,'refresh_token':refresh_token})
    
    @jwt_required(refresh=True)
    def put(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity, fresh=timedelta(minutes=5))
        return jsonify({'info':'access token bertambah 5 menit','access_token':access_token})


users_api = Blueprint('users', __name__)
api = Api(users_api)

api.add_resource(UserReg, '/user/register', endpoint='user/registr')
api.add_resource(User, '/user/signin', endpoint='user/signin')
