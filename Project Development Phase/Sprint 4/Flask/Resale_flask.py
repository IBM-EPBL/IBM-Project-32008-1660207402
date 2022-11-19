import pandas as pd
import numpy as np
from flask import Flask, render_template, Response, request
import pickle
from sklearn.preprocessing import LabelEncoder
import requests


app = Flask(__name__)#initiate flask app
# filename = '../resale_model.sav'
# model_rand = pickle.load (open (filename,'rb'))

API_KEY = "_UQf3F7bmy2SukTDfQ3TrfpHyqp4u3HXBjOJk69vC73s"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'}) 
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

  
@app.route('/')
def index():#main page
	return render_template('resaleintro.html')

@app.route('/predict')
def predict_page():#predicting page
	return render_template('resalepredict.html')


@app.route('/predicts', methods=['GET'])
def predict():
	reg_year = int(request.args.get('regyear'))
	powerps = float(request.args.get('powerps'))
	kms= float(request.args.get('kms'))
	reg_month = (request.args.get('regmonth'))

	gearbox = request.args.get('geartype')
	damage = request.args.get('damage')
	model = request.args.get('model')
	brand = request.args.get('brand')
	fuel_type = request.args.get('fuelType')
	veh_type = request.args.get('vehicletype')

	new_row = {'yearOfReg':reg_year, 'powerPS':powerps, 'kilometer':kms,
				'monthOfRegistration':reg_month, 'gearbox':gearbox,
				'notRepairedDamage':damage,
				'model':model, 'brand':brand, 'fuelType':fuel_type,
				'vehicletype':veh_type}

	print(new_row)

	new_df = pd.DataFrame(columns=['vehicletype','yearOfReg','gearbox',
		'powerPS','model','kilometer','monthOfRegistration','fuelType',
		'brand','notRepairedDamage'])
	new_df = new_df.append(new_row, ignore_index=True)
	labels = ['gearbox','notRepairedDamage','model','brand','fuelType','vehicletype']
	mapper = {}

	for i in labels:
		mapper[i] = LabelEncoder()
		mapper[i].classes = np.load('../'+str('classes'+i+'.npy'), allow_pickle=True)
		transform = mapper[i].fit_transform(new_df[i])
		new_df.loc[:,i+'_labels'] = pd.Series(transform, index=new_df.index)

	labeled = new_df[['yearOfReg','powerPS','kilometer','monthOfRegistration'] + [x+'_labels' for x in labels]]

	X = labeled.values.tolist()
	print('\n\n', X)
	payload_scoring = {"input_data": [{"field": [['yearOfRegistration', 'powerPS', 'kilometer',
       'monthOfRegistration', 'gearbox_labels', 'notRepairedDamage_labels',
       'model_labels', 'brand_labels', 'fuelType_labels',
       'vehicleType_labels']], "values": X}]}

	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f1a02296-819d-4106-8ea1-35bfcd286f8f/predictions?version=2022-11-12', json=payload_scoring,
	headers={'Authorization': 'Bearer ' + mltoken})
	predictions = response_scoring.json()
	print(predictions['predictions'][0]['values'][0][0]) 
	return render_template ('predict.html',predict = 'The resale value is {:.2f}$'.format(predictions['predictions'][0]['values'][0][0]))
    
if __name__ == '__main__':
    app.run()