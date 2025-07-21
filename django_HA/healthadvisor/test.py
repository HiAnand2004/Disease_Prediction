# test.py
import pandas as pd
import pickle
import numpy as np
from django.contrib.staticfiles import finders

def load_models():
    # Load processed dataset to get symptom names
    processed_data_path = finders.find("processed_data.csv")
    df = pd.read_csv(processed_data_path)
    symptom_columns = df.columns[1:]  # Extract symptom names

    # Load label encoder
    label_encoder_path = finders.find("label_encoder.pkl")
    with open(label_encoder_path, "rb") as f:
        label_encoder = pickle.load(f)

    # Load trained models
    models = {
        "Logistic_Regression": pickle.load(open(finders.find("Logistic_Regression.pkl"), "rb")),
        "Random_Forest": pickle.load(open(finders.find("Random_Forest.pkl"), "rb"))
    }
    
    return models, label_encoder, symptom_columns

def predict_disease(user_input_symptoms):
    models, label_encoder, symptom_columns = load_models()
    
    # Create input array (initialize with 0s)
    user_input_vector = np.zeros(len(symptom_columns), dtype="float32")

    # Set 1 for entered symptoms
    for symptom in user_input_symptoms:
        if symptom in symptom_columns:
            user_input_vector[list(symptom_columns).index(symptom)] = 1

    # Reshape for prediction
    user_input_vector = user_input_vector.reshape(1, -1)

    predictions = {}
    for name, model in models.items():
        prediction = model.predict(user_input_vector)
        disease = label_encoder.inverse_transform(prediction)[0]
        predictions[name] = disease
    
    return predictions