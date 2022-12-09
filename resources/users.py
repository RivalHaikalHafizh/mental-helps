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

class UserSignin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='email wajib ada',
            location=['json', 'args'],

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password wajib ada',
            location=['json', 'args'],

        )
        super().__init__()

class UserRegister(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='email wajib ada',
            location=['json', 'args'],

        )
        self.reqparse.add_argument(
            'username',
            required=True,
            help='username wajib ada',
            location=['json', 'args'],

        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='password wajib ada',
            location=['json', 'args'],

        )
        super().__init__()

class users(UserRegister):
    def post(self):
        args = self.reqparse.parse_args()
        email = args.get('email')
        username = args.get('username')
        password = args.get('password')
        try:
            models.User.select().where(models.User.email == email).get()
        except models.User.DoesNotExist:
            # daftarun usernya
            user = models.User.create(
                email=email,
                username=username,
                password=md5(password.encode('utf-8')).hexdigest()
            )
            additional_claims = {"aud": "some_audience", "foo": "bar"}
            access_token = create_access_token(email, additional_claims=additional_claims)
            info='anda sudah berhasil melakukan registrasi silahkan login untuk mendapatkan akses'
            return make_response(jsonify({'message':info,'result':True}),200)
        else:
            raise make_response(jsonify({'message':'email sudah terdaftar','result':False}),400)


class User(UserSignin):
    def post(self):
        args = self.reqparse.parse_args()
        email = args.get('email')
        password = args.get('password')
        try:
            hashpassword = md5(password.encode('utf-8')).hexdigest()
            email = models.User.get((models.User.email == email) & (
                models.User.password == hashpassword))
        except models.User.DoesNotExist:
            return make_response(jsonify({'message': 'user or passsword is wrong','result':False}),400)
        else:
            email = args.get('email')
            access_token = create_access_token(identity=email,fresh=True)
            refresh_token = create_refresh_token(identity=email)
            info='access token bertahan 1 jam dan refresh token bertahan 30 hari'
            return make_response(jsonify({'message':info,'result':True,'access_token':access_token,'refresh_token':refresh_token}),200)
    
    @jwt_required(refresh=True)
    def put(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity, fresh=timedelta(minutes=5))
        return make_response(jsonify({'message':'access token bertambah 5 menit','result':True,'access_token':access_token}),200)



users_api = Blueprint('users', __name__)
api = Api(users_api)

api.add_resource(users, '/user/register', endpoint='register')
api.add_resource(User, '/user/signin', endpoint='signin')
