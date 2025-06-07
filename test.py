import pandas as pd 
from joblib import load 


#Loading 
model = load('publishability.joblib')
scaler = load('scaler.pkl')

papers = pd.read_csv('Papers.csv')

names = papers['name']
input_papers = papers.drop(columns=['name'])

scaled_input = scaler.transform(input_papers)
predictions = model.predict(scaled_input)

input_papers['Name'] = names
input_papers['Publishability'] = predictions

print(input_papers)

input_papers.to_csv('publishability.csv', index=False)