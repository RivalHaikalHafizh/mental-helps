import pandas as pd 
import sklearn
import numpy as np 
from flask import Flask, jsonify, request
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
import joblib


pipe = joblib.load('model.pkl')
# New data to predict
d ={
    'Temprature':-0.877314,
    'Odor':1.2741591,
    'Fat ':0.729325,
    'Turbidity':1.434086,
    'merge':0.063744
}
pr = pd.DataFrame(d,index=[0])
pred_cols = list(pr.columns.values)[:]
# apply the whole pipeline to data
pred = pd.Series(pipe.predict(pr[pred_cols]))
print(pr)
print(f'hasil prediksi adalah {pred}')
    




