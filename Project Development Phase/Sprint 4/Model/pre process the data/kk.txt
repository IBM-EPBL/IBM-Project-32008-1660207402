import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "_UQf3F7bmy2SukTDfQ3TrfpHyqp4u3HXBjOJk69vC73s"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [['yearOfRegistration', 'powerPS', 'kilometer',
       'monthOfRegistration', 'gearbox_labels', 'notRepairedDamage_labels',
       'model_labels', 'brand_labels', 'fuelType_labels',
       'vehicleType_labels']], "values": [[2015, 234.0, 38593.0, '3', 0, 0, 0, 0, 0, 0]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f1a02296-819d-4106-8ea1-35bfcd286f8f/predictions?version=2022-11-12', json=payload_scoring,
headers={'Authorization': 'Bearer ' + mltoken})
predictions = response_scoring.json()
print(predictions['predictions'][0]['values'][0][0])