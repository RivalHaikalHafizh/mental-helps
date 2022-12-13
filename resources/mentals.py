from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (
    Resource,
    Api,
    reqparse,
    fields,
    marshal,
    marshal_with,
)
from category_encoders import *
import json
import tensorflow as tf
import logging
import pickle
from operator import itemgetter
from flask_cors import CORS, cross_origin
import pandas as pd
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
import models

mental_fields = {
    "Age": fields.String,
    "Educational_level": fields.String,
    "Screening_time": fields.String,
    "lack_of_practical_exposure": fields.String,
    "Exercise": fields.String,
    "depressiveness": fields.String,
    "unnecessary_misunderstandings": fields.String,
    "online_courses": fields.String,
    "overthinking": fields.String,
    "social_media_hours": fields.Integer,
    "hobby_hours": fields.Integer,
    "increased_sleep_hours": fields.Integer,
    "health_problems": fields.String,
}


class UserBase(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "Age",
            required=True,
            help="Age wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "Educational_level",
            required=True,
            help="Educational_level wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "Screening_time",
            required=True,
            help="Screening_time wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "Irregular_eating_habits",
            required=True,
            help="Irregular_eating_habits wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "Exercise",
            required=True,
            help="Exercise wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "depressiveness",
            required=True,
            help="depressiveness wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "unnecessary_misunderstandings",
            required=True,
            help="unnecessary_misunderstandings wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "online_courses",
            required=True,
            help="online_courses wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "overthinking",
            required=True,
            help="overthinking wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "social_media_hours",
            required=True,
            help="social_media_hours wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "hobby_hours",
            required=True,
            help="hobby_hours wajib ada",
            location=["json"],
        )
        self.reqparse.add_argument(
            "increased_sleep_hours",
            required=True,
            help="increased_sleep_hours wajib ada",
            location=["json"],
        )

    def descr(d):
        hasil = ""
        if d == "Yes":
            hasil = (
                "Kesehatan mental kamu sedang tidak baik mungkin kamu berada"
                " di bawah banyak tekanan sekarang,merasa lebih takut dari"
                " yang bisa kamu tangani. Masalah yang kamu hadapi membuat"
                " kamu kurang nyaman dan kurang bisa melakukan aktivitas"
                " sehari-hari dan Mungkin kamu juga merasa tidak berdaya dalam"
                " menyelesaikan permasalahan yang kamu hadapi."
            )
        else:
            hasil = (
                "Saat ini kamu boleh dibilang tidak ada masalah kesehatan"
                " mental. Kamu merasa nyaman dengan hidupmu. Kamu juga bisa"
                " berkegiatan dengan baik dan produktif. Selain itu, kamu juga"
                " cenderung memiliki kontrol penuh terhadap hidupmu."
            )
        return hasil

    def solusi(d):
        solusi = {}
        eat, exe, dep, ove, inc = itemgetter(
            "Irregular_eating_habits",
            "Exercise",
            "depressiveness",
            "overthinking",
            "increased_sleep_hours",
        )(d)
        if eat == "Yes" or eat == "May be":
            solusi["eat"] = (
                "Melewatkan sarapan berdampak buruk bagi kesehatan mental"
                " kamu. Sarapan teratur membantu mengisi ulang tubuh dan otak"
                " kamu. Setelah tidur panjang, makanan menjadi metabolisme"
                " kamu untuk hari itu Melewatkan sarapan menyebabkan kelelahan"
                " dan menimbulkan perasaan berbeda,begitu juga makan siang dan"
                " malam harus tepat waktu dan memenuhi nutrisi harian kamu"
            )
        else:
            solusi["eat"] = (
                "Kamu hebat! Pola makanmu cukup bagus. Itu sangat mempengaruhi"
                " kesehatan mental kamu lebih sehat lagi."
            )
        if exe == "Never" or exe == "Rarely":
            solusi["exe"] = (
                " Kamu masih kurang aktif secara fisik (jarang berolahraga"
                " dengan rutin dan lebih memilih untuk  tidak banyak bergerak)"
                " sehingga kamu perlu mengubahnya."
            )
        else:
            solusi["exe"] = (
                "Kamu hebat! Kamu sudah aktif secara fisik (rajin berolahraga"
                " dan lebih memilih untuk banyak bergerak)."
            )
        if dep == "Never" or dep == "Rarely":
            solusi["dep"] = (
                "Saat ini kamu tidak memiliki, atau sangat sedikit gejala"
                " depresi. Memiliki suasana hati yang rendah atau perasaan"
                " gelisah adalah pengalaman umum bagi kita semua. Mungkin"
                " bermanfaat jika Anda dapat menjangkau teman dan keluarga"
                " terpercaya. Namun, kami tetap menyarankan Anda untuk cukup"
                " memperhatikan kesehatan mental Anda. Jangan ragu untuk"
                " meminta profesional setiap kali Anda merasa gelombang mood"
                " luar biasa.Kamu merasa nyaman dengan hidupmu."
            )
        else:
            solusi["dep"] = (
                "Dilihat dari gejala yang kamu alami, kamu harus segera"
                " mencari bantuan. Kami sangat menyarankan kamu untuk"
                " berbicara dengan seseorang yang mungkin dapat membantu."
                " Hubungi teman dan keluargamu atau jika kamu pikir mereka"
                " akan memahamimu, konsultasi saja dengan dokter umum. Dia"
                " dapat membantumu menjelajahi pilihanmu, memahami masalahmu"
                " lebih baik, atau hanya mendengarkan keluh kesahmu."
            )
        if ove == "Yes" or ove == "May be":
            solusi["ove"] = (
                "kamu memikirkan pikiran negatif berulang kali. Kamu juga"
                " tidak bisa mengendalikannya. Kamu  terlalu fokus pada"
                " peristiwa dan perasaan negatif yang kamu alami. Hal ini"
                " terkadang membuat aktivitas sehari-hari, seperti"
                " berkonsentrasi, menjadi sulit. "
            )
        else:
            solusi["ove"] = (
                "Kamu dapat mengendalikan pikiran-pikiran negatifmu dengan"
                " baik. Kamu tidak terlalu fokus pada kejadian dan perasaan"
                " negatif yang pernah kamu alami."
            )
        if inc == "4" or inc == "3":
            solusi["inc"] = (
                "Kamu hebat! Kualitas tidurmu sudah baik karena kamu mudah"
                " untuk bisa terlelap dan tertidur kembali jika kamu terbangun"
                " di malam atau dini hari. Oleh karena itu, lanjutkan pola"
                " tidurmu yang sudah sehat ini."
            )
        else:
            solusi["inc"] = (
                "Kualitas tidurmu masih perlu ditingkatkan karena kamu masih"
                " sulit untuk bisa terlelap bahkan sulit untuk tertidur"
                " kembali jika kamu terbangun di malam atau dini hari."
            )
        return solusi
        super().__init__()


class Mental(UserBase):
    def post(self):
        model = None
        label = ["Yes", "No"]
        model = tf.keras.models.load_model(r"./model.h5")
        args = self.reqparse.parse_args()
        Age = args.get("Age")
        Educational_level = args.get("Educational_level")
        Screening_time = args.get("Screening_time")
        Irregular_eating_habits = args.get("Irregular_eating_habits")
        Exercise = args.get("Exercise")
        depressiveness = args.get("depressiveness")
        unnecessary_misunderstandings = args.get(
            "unnecessary_misunderstandings"
        )
        online_courses = args.get("online_courses")
        overthinking = args.get("overthinking")
        social_media_hours = args.get("social_media_hours")
        hobby_hours = args.get("hobby_hours")
        increased_sleep_hours = args.get("increased_sleep_hours")
        health_problems = "yes"
        dict_data = {
            "Age": Age,
            "Educational_level": Educational_level,
            "Screening_time": Screening_time,
            "Irregular_eating_habits": Irregular_eating_habits,
            "Exercise": Exercise,
            "depressiveness": depressiveness,
            "overthinking": overthinking,
            "unnecessary_misunderstandings": unnecessary_misunderstandings,
            "online_courses": online_courses,
            "social_media_hours": int(social_media_hours),
            "hobby_hours": int(hobby_hours),
            "increased_sleep_hours": int(increased_sleep_hours),
            "health_problems": health_problems,
        }
        df_data = pd.DataFrame(dict_data, index=[0])
        # encoder
        file = open(f"./enc.pkl", "rb")
        enc = pickle.load(file)
        file.close()
        categorical_features = [
            "Age",
            "Educational_level",
            "Screening_time",
            "Irregular_eating_habits",
            "Exercise",
            "depressiveness",
            "overthinking",
            "unnecessary_misunderstandings",
            "online_courses",
            "health_problems",
        ]
        df_deploy_encoded = enc.transform(df_data[categorical_features])
        df_data[categorical_features] = df_deploy_encoded
        # scaler
        file = open(f"./scaler.pkl", "rb")
        scaler = pickle.load(file)
        file.close()
        numerical_features = [
            "social_media_hours",
            "hobby_hours",
            "increased_sleep_hours",
        ]
        df_data[numerical_features] = scaler.transform(
            df_data.loc[:, numerical_features]
        )
        df_data_sample = df_data.drop("health_problems", axis=1)
        # # apply the whole pipeline to data

        if model is None:
            return jsonify("Model Belum Siap")
        data_prediksi = model.predict(df_data_sample)[0]

        detail_pred = []
        for i in range(len(data_prediksi)):
            detail_pred.append(
                {"class": label[i], "confidence": str(data_prediksi[i])}
            )
        if detail_pred[0]["confidence"] > detail_pred[1]["confidence"]:
            hasil = detail_pred[0]["class"]
        else:
            hasil = detail_pred[1]["class"]

        solusi = UserBase.solusi(dict_data)
        desc = UserBase.descr(hasil)
        models.MentalHelps.create(
            Age=Age,
            Educational_level=Educational_level,
            Screening_time=Screening_time,
            Irregular_eating_habits=Irregular_eating_habits,
            Exercise=Exercise,
            depressiveness=depressiveness,
            unnecessary_misunderstandings=unnecessary_misunderstandings,
            online_courses=online_courses,
            overthinking=overthinking,
            social_media_hours=social_media_hours,
            hobby_hours=hobby_hours,
            increased_sleep_hours=increased_sleep_hours,
            health_problems=hasil,
        )
        return make_response(
            jsonify(
                {"hasilprediksi": hasil, "solusi": solusi, "deskripsi": desc}
            ),
            200,
        )


class MentalInfo(UserBase):
    def get(self):
        mentals = [
            marshal(mental, mental_fields)
            for mental in models.MentalHelps.select()
        ]
        # print("MENTALS: ", mentals)
        return make_response(jsonify({"mentalsdata": mentals}), 200)


mentals_api = Blueprint("mentals", __name__)
api = Api(mentals_api)

api.add_resource(Mental, "/models/predict", endpoint="predict")
api.add_resource(MentalInfo, "/models/info", endpoint="info")
