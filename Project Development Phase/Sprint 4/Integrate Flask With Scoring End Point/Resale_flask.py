import pandas as pd
import numpy as np
from flask import Flask, render_template, request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "_VdiGGVE2riXwMsv4Otfb1PoHBp7TgTkxl0ff__UheDS"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

#model=pickle.load(open('RandomForest.pkl','rb'))
car=pd.read_csv('Cleaned.csv')

@app.route('/')
def index():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(),reverse=True)
    fuel_type=car['fuel_type'].unique()

    companies.insert(0,'Select Company')
    return render_template('index.html',companies=companies, car_models=car_models, years=year,fuel_types=fuel_type)


@app.route('/predict',methods=['POST'])
def predict():

    company=request.form.get('company')

    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=request.form.get('kilo_driven')

    # NOTE: manually define and pass the array(s) of values to be scored in the next line

    payload_scoring = {"input_data": [{"fields": ['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                                       "values": [[car_model, company, year, driven, fuel_type]]}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0a769d98-9edf-4e48-bf5c-f371da57233b/predictions?version=2022-11-18',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    #prediction = response_scoring['predictions'][0]['values']
    pred = response_scoring.json()
    #return pred['predictions'][0]['values'][0][0]
    return str(np.round(pred['predictions'][0]['values'][0][0]))



if __name__=='__main__':
    app.run()