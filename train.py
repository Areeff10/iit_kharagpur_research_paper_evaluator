import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
from joblib import dump

pub = pd.read_csv('Publishable.csv')
nonpub = pd.read_csv('Non-Publishable.csv')

pub['publishability'] = 1
nonpub['publishability'] = 0

references = pd.concat([pub,nonpub])

X = references[['pages', 'sections', 'subSections', 'size']]
Y = references['publishability']


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

print("Scores : ")
print(classification_report(Y_test, Y_pred))
print("AUC-ROC Score:", roc_auc_score(Y_test, model.predict_proba(X_test)[:, 1]))


X_test_original = scaler.inverse_transform(X_test)  # Optionally revert scaling for interpretability
results = pd.DataFrame(X_test_original, columns=['pages', 'sections', 'subSections', 'size'])
results['Prediction'] = Y_pred
results['Actual'] = Y_test.reset_index(drop=True)

print("Results :")
print(results)

#Saving
dump(model, 'publishability.joblib')
dump(scaler, "scaler.pkl")