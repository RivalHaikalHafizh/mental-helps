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
    # 'Irregular_eating_habits':fields.String,
    'Exercise':fields.String,
    'depressiveness':fields.String,
    'unnecessary_misunderstandings':fields.String,
    'online_courses':fields.String,
    # 'procrastination':fields.Integer,
    'overthinking':fields.Integer,
    'social_media_hours':fields.Integer,
    'hobby_hours':fields.Integer,
    'increased_sleep_hours':fields.Integer,
    # 'online_difficulty_level':fields.Integer,
    # 'focus_level':fields.Integer,
    'health_problems': fields.String
}

class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'Age',
            required=True,
            help='Age wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'Educational_level',
            required=True,
            help='Educational_level wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'Screening_time',
            required=True,
            help='Screening_time wajib ada',
            location=['json'],

        )
        # self.reqparse.add_argument(
        #     'lack_of_practical_exposure',
        #     required=True,
        #     help='lack_of_practical_exposure wajib ada',
        #     location=['json'],

        # )
        self.reqparse.add_argument(
            'Irregular_eating_habits',
            required=True,
            help='Irregular_eating_habits wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'Exercise',
            required=True,
            help='Exercise wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'depressiveness',
            required=True,
            help='depressiveness wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'unnecessary_misunderstandings',
            required=True,
            help='unnecessary_misunderstandings wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'online_courses',
            required=True,
            help='online_courses wajib ada',
            location=['json'],

        )
        # self.reqparse.add_argument(
        #     'procrastination',
        #     required=True,
        #     help='procrastination wajib ada',
        #     location=['json'],

        # )
        self.reqparse.add_argument(
            'overthinking',
            required=True,
            help='overthinking wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'social_media_hours',
            required=True,
            help='social_media_hours wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'hobby_hours',
            required=True,
            help='hobby_hours wajib ada',
            location=['json'],

        )
        self.reqparse.add_argument(
            'increased_sleep_hours',
            required=True,
            help='increased_sleep_hours wajib ada',
            location=['json'],

        )
        # self.reqparse.add_argument(
        #     'online_difficulty_level',
        #     required=True,
        #     help='online_difficulty_level wajib ada',
        #     location=['json'],

        # )
        # self.reqparse.add_argument(
        #     'focus_level',
        #     required=True,
        #     help='focus_level wajib ada',
        #     location=['json'],

        # )
        super().__init__()


class Mental(UserBase):
    def post(self):
        args = self.reqparse.parse_args()
        Age = args.get('Age')
        Educational_level = args.get('Educational_level')
        Screening_time  = args.get('Screening_time')
        Irregular_eating_habits = args.get('Irregular_eating_habits')
        Exercise = args.get('Exercise')
        depressiveness = args.get('depressiveness')
        unnecessary_misunderstandings = args.get('unnecessary_misunderstandings')
        online_courses  = args.get('online_courses')
        overthinking = args.get('overthinking')
        social_media_hours = args.get('social_media_hours')
        hobby_hours = args.get('hobby_hours')
        increased_sleep_hours= args.get('increased_sleep_hours')
        pipe = load('../mental-helps/model.joblib')
        d = {
                'Age':Age,
                'Educational_level': Educational_level,
                'Screening_time': Screening_time,
                'Irregular_eating_habits':Irregular_eating_habits,
                'Exercise':Exercise,
                'depressiveness':depressiveness,
                'overthinking': overthinking,
                'unnecessary_misunderstandings':unnecessary_misunderstandings,
                'online_courses':online_courses,
                'social_media_hours': int(social_media_hours),
                'hobby_hours': int(hobby_hours),
                'increased_sleep_hours': int(increased_sleep_hours),
            }
        pr = pd.DataFrame(d, index=[0])
        #encoder
        pr['Age']=pr['Age'].map({'16 to 18 years': 1,'18 to 22 years': 2,'13 to 15 years': 0,'23 to 26 years': 3})
        pr['Educational_level']= pr['Educational_level'].map({'Higher Secondary School': 0,'Under Graduate': 3,'Secondary School': 2,'Post Graduate': 1})
        pr['Screening_time']=pr['Screening_time'].map( {'2 to 3 hours': 0,'4 to 5 hours': 2,'3 to 4 hours': 1,'5 to 6 hours': 3})
        pr['Irregular_eating_habits']=pr['Irregular_eating_habits'].map({'Yes': 2, 'No': 1, 'May be': 0})
        pr['Exercise']=pr['Exercise'].map({'Rarely': 2, 'Sometimes': 3, 'Never': 1, 'Always': 0})
        pr['depressiveness']=pr['depressiveness'].map({'Occasionally': 2,'Never': 1,'All the time': 0,'Rarely': 3})
        pr['overthinking']=pr['overthinking'].map({'Yes': 2, 'No': 1, 'May be': 0})
        pr['unnecessary_misunderstandings']=pr['unnecessary_misunderstandings'].map({'No': 1, 'Yes': 2, 'Maybe': 0})
        pr['online_courses']=pr['online_courses'].map({'1': 1, '0': 0, 'more than 3': 4, '2': 2, '3': 3})
        # categorical_features=['Age', 'Educational_level', 'Screening_time', 'Irregular_eating_habits', 'Exercise', 'depressiveness','unnecessary_misunderstandings','online_courses']
        # label_encoders = {}
        # enc = load('../mental-helps/encoder.joblib') 
        # for col in pr[categorical_features]:
        #     pr.replace(enc[col], inplace=True)
        #encode=pr.to_dict('records')
        #scaler
        same_standard_scaler = load('../mental-helps/scaler.joblib') 
        numerical_features = ['social_media_hours', 'hobby_hours','increased_sleep_hours']
        pr[numerical_features] = same_standard_scaler.transform(pr.loc[:, numerical_features])
        pred_cols = list(pr.columns.values)[:]
        # # apply the whole pipeline to data
        pred = pd.Series(pipe.predict(pr[pred_cols]))
        health_problem =pred[0]
        mentals = models.MentalHelps.create(
            Age=Age,
            Educational_level=Educational_level,
            Screening_time=Screening_time,
            # lack_of_practical_exposure=lack_of_practical_exposure,
            Irregular_eating_habits=Irregular_eating_habits,
            Exercise=Exercise,
            depressiveness=depressiveness,
            unnecessary_misunderstandings=unnecessary_misunderstandings,
            online_courses=online_courses,
            # procrastination=procrastination,
            overthinking=overthinking,
            social_media_hours=social_media_hours,
            hobby_hours=hobby_hours,
            increased_sleep_hours=increased_sleep_hours,
            # online_difficulty_level=online_difficulty_level,
            # focus_level=focus_level,
            health_problems=health_problem
        )
        return make_response(jsonify({'featureanda':d,'hasilprediksi':health_problem}),200)

class MentalInfo(UserBase):   
    def get(self):
        mentals=[marshal(mental,mental_fields)for mental in models.MentalHelps.select()]
        return make_response(jsonify({'mentalsdata':mentals}),200)




mentals_api = Blueprint('mentals', __name__)
api = Api(mentals_api)

api.add_resource(Mental, '/models/predict', endpoint='predict')
api.add_resource(MentalInfo, '/models/info', endpoint='info')
