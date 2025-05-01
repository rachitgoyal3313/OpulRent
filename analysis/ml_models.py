import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# === Constants ===
MODEL_DIR = "ml_models"
RENT_MODEL_FILE = os.path.join(MODEL_DIR, "rent_model.pkl")
GROWTH_MODEL_FILE = os.path.join(MODEL_DIR, "growth_model.pkl")

# === Ensure model directory exists ===
os.makedirs(MODEL_DIR, exist_ok=True)

# === Load and preprocess dataset ===
def load_and_preprocess_data(filepath):
    df = pd.read_excel(filepath)

    # Compute Growth Score (/10 scale)
    min_rate = df["area_rate"].min()
    max_rate = df["area_rate"].max()
    df["growth_score"] = 10 * (df["area_rate"] - min_rate) / (max_rate - min_rate)
    df["growth_score"] = df["growth_score"].clip(0, 10)

    # Features and targets
    X = df.drop(columns=["rent", "growth_score"])
    y_rent = df["rent"]
    y_growth = df["growth_score"]

    return X, y_rent, y_growth

# === Preprocessing Pipeline ===
categorical_features = ["type", "locality", "city", "furnishing"]
numerical_features = ["bhk", "area", "beds", "bathrooms", "balconies", "area_rate"]

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'
)

# === Train and Save Models ===
def train_and_save_models(filepath):
    X, y_rent, y_growth = load_and_preprocess_data(filepath)
    X_train, X_test, y_rent_train, y_rent_test = train_test_split(X, y_rent, test_size=0.2, random_state=42)
    _, _, y_growth_train, y_growth_test = train_test_split(X, y_growth, test_size=0.2, random_state=42)

    def train_model(X_train, y_train):
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
        ])
        pipeline.fit(X_train, y_train)
        return pipeline

    rent_model = train_model(X_train, y_rent_train)
    growth_model = train_model(X_train, y_growth_train)

    joblib.dump(rent_model, RENT_MODEL_FILE)
    joblib.dump(growth_model, GROWTH_MODEL_FILE)

    print("✅ Models trained and saved.")

# === ROI Calculation ===
def calculate_roi(area, area_rate, predicted_rent):
    investment = area * area_rate
    annual_rent = predicted_rent
    roi = ((annual_rent / 12) / investment) * 100
    return roi

# === Prediction Function ===
def predict_property(type_, locality, city, furnishing, bhk, area, beds, bathrooms, balconies, area_rate):
    # Load models
    if not os.path.exists(RENT_MODEL_FILE) or not os.path.exists(GROWTH_MODEL_FILE):
        raise FileNotFoundError("Models not found. Train the models first using train_and_save_models().")

    rent_model = joblib.load(RENT_MODEL_FILE)
    growth_model = joblib.load(GROWTH_MODEL_FILE)

    input_data = pd.DataFrame([{
        "type": type_,
        "locality": locality,
        "city": city,
        "furnishing": furnishing,
        "bhk": bhk,
        "area": area,
        "beds": beds,
        "bathrooms": bathrooms,
        "balconies": balconies,
        "area_rate": area_rate
    }])

    predicted_rent = rent_model.predict(input_data)[0]
    predicted_growth = growth_model.predict(input_data)[0]
    predicted_roi = calculate_roi(area, area_rate, predicted_rent)

    return {
        "predicted_rent": round(predicted_rent / 12, 2),
        "predicted_roi": round(predicted_roi, 2),
        "predicted_growth": round(predicted_growth)
    }

# === Optional: Example Run ===
if _name_ == "_main_":
    dataset_path = "cities_magicbricks_rental_prices_updated.xlsx"
    train_and_save_models(dataset_path)

    result = predict_property(
        type_="Flat",
        locality="Goregaon",
        city="Mumbai",
        furnishing="furnished",
        bhk=2,
        area=1000,
        beds=2,
        bathrooms=1,
        balconies=1,
        area_rate=3000
    )

    print("\n🔍 Prediction for Input Property:")
    print(f"Estimated Rent: ₹{result['predicted_rent']:,.2f}/month")
    print(f"Estimated ROI: {result['predicted_roi']}% annually")
    print(f"Growth Potential: {result['predicted_growth']}/10")