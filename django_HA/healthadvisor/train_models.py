import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("processed_data.csv")

# Ensure the first column is 'Disease' (Target), and the rest are features
X = df.iloc[:, 1:]  # Symptoms (features)
y = df.iloc[:, 0]   # Disease (target)

# Convert X to float32 to save memory
X = X.astype("float32")

# Encode the disease column (target variable)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Save label encoder for decoding predictions later
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Define models with optimized parameters
models = {
    "Logistic_Regression": LogisticRegression(max_iter=500),
    "Random_Forest": RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)  # Reduced depth
}

# Train and save models
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    with open(f"{name}.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"{name} model saved.")

print("Training complete. Models saved as .pkl files.")
