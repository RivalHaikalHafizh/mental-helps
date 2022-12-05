from flask import jsonify, Blueprint, abort,make_response
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with
import json
from flask_cors import CORS,cross_origin
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from flask_jwt_extended import JWTManager, jwt_required,create_access_token, get_jwt_identity
from joblib import dump, load  
import models

mental_fields = {
    'Age':fields.String,
    'Educational_level':fields.String,
    'Screening_time':fields.String,
    'lack_of_practical_exposure':fields.String,
    'Irregular_eating_habits':fields.String,
    'Exercise':fields.String,
    'depressiveness':fields.String,
    'unnecessary_misunderstandings':fields.String,
    'online_courses':fields.String,
    'procrastination':fields.Integer,
    'social_media_hours':fields.Integer,
    'hobby_hours':fields.Integer,
    'increased_sleep_hours':fields.Integer,
    'online_difficulty_level':fields.Integer,
    'focus_level':fields.Integer,
    'health_problems': fields.String
}

class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'Age',
            required=True,
            help='Age wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'Educational_level',
            required=True,
            help='Educational_level wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'Screening_time',
            required=True,
            help='Screening_time wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'lack_of_practical_exposure',
            required=True,
            help='lack_of_practical_exposure wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'Irregular_eating_habits',
            required=True,
            help='Irregular_eating_habits wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'Exercise',
            required=True,
            help='Exercise wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'depressiveness',
            required=True,
            help='depressiveness wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'unnecessary_misunderstandings',
            required=True,
            help='unnecessary_misunderstandings wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'online_courses',
            required=True,
            help='online_courses wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'procrastination',
            required=True,
            help='procrastination wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'social_media_hours',
            required=True,
            help='social_media_hours wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'hobby_hours',
            required=True,
            help='hobby_hours wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'increased_sleep_hours',
            required=True,
            help='increased_sleep_hours wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'online_difficulty_level',
            required=True,
            help='online_difficulty_level wajib ada',
            location=['form'],

        )
        self.reqparse.add_argument(
            'focus_level',
            required=True,
            help='focus_level wajib ada',
            location=['form'],

        )
        super().__init__()


class Mental(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        Age = args.get('Age')
        Educational_level = args.get('Educational_level')
        Screening_time  = args.get('Screening_time')
        lack_of_practical_exposure = args.get('lack_of_practical_exposure')
        Irregular_eating_habits = args.get('Irregular_eating_habits')
        Exercise = args.get('Exercise')
        depressiveness = args.get('depressiveness')
        unnecessary_misunderstandings = args.get('unnecessary_misunderstandings')
        online_courses  = args.get('online_courses')
        procrastination = args.get('procrastination')
        social_media_hours = args.get('social_media_hours')
        hobby_hours = args.get('hobby_hours')
        increased_sleep_hours= args.get('increased_sleep_hours')
        online_difficulty_level = args.get('online_difficulty_level')
        focus_level = args.get('focus_level')
        pipe = load('../mental-helps/model.joblib')
        d = {
                'Age':Age,
                'Educational_level': Educational_level,
                'Screening_time': Screening_time,
                'lack_of_practical_exposure': lack_of_practical_exposure,
                'Irregular_eating_habits':Irregular_eating_habits,
                'Exercise':Exercise,
                'depressiveness':depressiveness,
                'unnecessary_misunderstandings':unnecessary_misunderstandings,
                'online_courses':online_courses,
                'procrastination': int(procrastination),
                'social_media_hours': int(social_media_hours),
                'hobby_hours': int(hobby_hours),
                'increased_sleep_hours': int(increased_sleep_hours),
                'online_difficulty_level': int(online_difficulty_level),
                'focus_level': int(focus_level),
            }
        pr = pd.DataFrame(d, index=[0])
        #encoder
        categorical_features=['Age', 'Educational_level', 'Screening_time', 'lack_of_practical_exposure', 'Irregular_eating_habits', 'Exercise', 'depressiveness','unnecessary_misunderstandings','online_courses']
        label_encoders = {}
        enc = load('../mental-helps/encoder.joblib') 
        for col in pr[categorical_features]:
            pr.replace(enc[col], inplace=True)
        #encode=pr.to_dict('records')
        #scaler
        same_standard_scaler = load('../mental-helps/scaler.joblib') 
        pr[:] = same_standard_scaler.transform(pr.loc[:])
        pred_cols = list(pr.columns.values)[:]
        # # apply the whole pipeline to data
        pred = pd.Series(pipe.predict(pr[pred_cols]))
        health_problem =pred[0]
        mentals = models.MentalHelps.create(
            Age=Age,
            Educational_level=Educational_level,
            Screening_time=Screening_time,
            lack_of_practical_exposure=lack_of_practical_exposure,
            Irregular_eating_habits=Irregular_eating_habits,
            Exercise=Exercise,
            depressiveness=depressiveness,
            unnecessary_misunderstandings=unnecessary_misunderstandings,
            online_courses=online_courses,
            procrastination=procrastination,
            social_media_hours=social_media_hours,
            hobby_hours=hobby_hours,
            increased_sleep_hours=increased_sleep_hours,
            online_difficulty_level=online_difficulty_level,
            focus_level=focus_level,
            health_problems=health_problem
        )
        return make_response(jsonify({'feature anda':d,'health problem hasil prediksi':health_problem}),200)

class MentalInfo(UserBase):   
    @jwt_required()
    def get(self):
        mentals=[marshal(mental,mental_fields)for mental in models.MentalHelps.select()]
        return make_response(jsonify({'mentalsdata':mentals}),200)




mentals_api = Blueprint('mentals', __name__)
api = Api(mentals_api)

api.add_resource(Mental, '/models/predict', endpoint='predict')
api.add_resource(MentalInfo, '/models/info', endpoint='info')
