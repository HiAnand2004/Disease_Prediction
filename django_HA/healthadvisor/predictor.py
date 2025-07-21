# healthadvisor/predictor.py

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load your models and data
DATA_PATH = "illnessnames/file2.csv"
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# Encoding the target value
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])

# Splitting the data
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Training models on the whole dataset
final_svm_model = SVC()
final_nb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)

final_svm_model.fit(X, y)
final_nb_model.fit(X, y)
final_rf_model.fit(X, y)

# Creating a symptom index dictionary
symptoms = X.columns.values
symptom_index = {symptom.replace("_", " ").capitalize(): i for i, symptom in enumerate(symptoms)}

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}

# Function to predict disease from symptoms
def predict_disease(symptoms_input):
    symptoms_list = [s.strip().capitalize() for s in symptoms_input.split(",") if s.strip()]
    
    # Creating input vector for the model
    input_data = [0] * len(symptom_index)
    for symptom in symptoms_list:
        index = symptom_index.get(symptom, None)
        if index is not None:
            input_data[index] = 1

    # Making predictions
    input_data = pd.DataFrame([input_data], columns=symptoms)
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_nb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    return {
        "rf_prediction": rf_prediction,
        "nb_prediction": nb_prediction,
        "svm_prediction": svm_prediction
    }