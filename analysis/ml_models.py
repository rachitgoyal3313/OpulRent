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
# Path to dataset relative to ml_models.py (up one directory to project root)
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cities_magicbricks_rental_prices.xlsx")

# === Ensure model directory exists ===
os.makedirs(MODEL_DIR, exist_ok=True)

# === Load and preprocess dataset ===
def load_and_preprocess_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file {filepath} not found.")
    
    # Print debugging info about the dataset
    print(f"Loading dataset from {filepath}")
    
    df = pd.read_excel(filepath)
    
    # Print column names to debug
    print(f"Dataset columns: {df.columns.tolist()}")
    
    # Compute Growth Score (/10 scale) - Ensuring area_rate is properly normalized
    df["area_rate"] = pd.to_numeric(df["area_rate"], errors='coerce')
    
    # Handle potential missing or invalid values
    df["area_rate"] = df["area_rate"].fillna(df["area_rate"].median())
    
    # Ensure we have a range for normalization
    min_rate = df["area_rate"].min()
    max_rate = df["area_rate"].max()
    
    # Prevent division by zero if min_rate equals max_rate
    if min_rate == max_rate:
        df["growth_score"] = 5.0  # Default middle value if all rates are the same
    else:
        df["growth_score"] = 10 * (df["area_rate"] - min_rate) / (max_rate - min_rate)
    
    df["growth_score"] = df["growth_score"].clip(0, 10)
    print(f"Growth score range: {df['growth_score'].min()} to {df['growth_score'].max()}")

    # Features and targets
    X = df.drop(columns=["rent", "growth_score"])
    y_rent = df["rent"]
    y_growth = df["growth_score"]

    return X, y_rent, y_growth

# === Preprocessing Pipeline ===
# This will be adjusted based on actual columns in the dataset
def get_preprocessor(X):
    # Detect categorical and numerical features
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    print(f"Categorical features: {categorical_features}")
    print(f"Numerical features: {numerical_features}")
    
    # Make sure we have at least one categorical feature
    if len(categorical_features) == 0:
        print("Warning: No categorical features detected. Using default processing.")
        preprocessor = ColumnTransformer(
            transformers=[],
            remainder='passthrough'
        )
    else:
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ],
            remainder='passthrough'
        )
    
    return preprocessor

# === Train and Save Models ===
def train_and_save_models(filepath):
    try:
        X, y_rent, y_growth = load_and_preprocess_data(filepath)
        X_train, X_test, y_rent_train, y_rent_test = train_test_split(X, y_rent, test_size=0.2, random_state=42)
        _, _, y_growth_train, y_growth_test = train_test_split(X, y_growth, test_size=0.2, random_state=42)

        def train_model(X_train, y_train):
            # Get preprocessor based on actual data columns
            preprocessor = get_preprocessor(X_train)
            
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
    except Exception as e:
        import traceback
        print(f"Training error: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"Failed to train models: {str(e)}")

# === ROI Calculation ===
def calculate_roi(area, area_rate, predicted_rent):
    investment = area * area_rate
    annual_rent = predicted_rent
    roi = ((annual_rent / 12) / investment) * 100
    return roi

# === Prediction Function ===
def predict_property(type_, locality, city, furnishing, bhk, area, beds, bathrooms, balconies, area_rate):
    # Check if models exist, train if they don't
    if not os.path.exists(RENT_MODEL_FILE) or not os.path.exists(GROWTH_MODEL_FILE):
        if os.path.exists(DATASET_PATH):
            print(f"Models not found. Training new models using dataset: {DATASET_PATH}")
            train_and_save_models(DATASET_PATH)
        else:
            raise FileNotFoundError(f"Dataset {DATASET_PATH} not found. Please ensure the dataset is available to train the models.")

    # Load models
    try:
        rent_model = joblib.load(RENT_MODEL_FILE)
        growth_model = joblib.load(GROWTH_MODEL_FILE)
    except Exception as e:
        raise Exception(f"Failed to load models: {str(e)}")

    input_data = pd.DataFrame([{
        "house_type": type_,  # Changed from "type" to "house_type" to match dataset
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
    # Ensure area_rate is numeric and properly handled
    input_data['area_rate'] = pd.to_numeric(input_data['area_rate'], errors='coerce')
    
    # Make prediction with growth_model
    try:
        predicted_growth = growth_model.predict(input_data)[0]
        # Ensure the growth score is within reasonable bounds (0-10)
        predicted_growth = max(0, min(10, predicted_growth))
    except Exception as e:
        print(f"Error predicting growth: {str(e)}")
        # Fallback calculation if model prediction fails
        # Simple heuristic: higher area_rate tends to correlate with higher growth
        if pd.notna(area_rate) and area_rate > 0:
            # You would need to calibrate this based on your specific dataset
            predicted_growth = min(10, max(1, area_rate / 1000))
        else:
            predicted_growth = 5.0  # Default middle value

    predicted_roi = calculate_roi(area, area_rate, predicted_rent)

    return {
        "predicted_rent": round(predicted_rent / 12, 2),
        "predicted_roi": round(predicted_roi, 2),
        "predicted_growth": round(predicted_growth, 1)  # Changed to 1 decimal place for better precision
    }

# === Optional: Example Run ===
if __name__ == "__main__":
    if os.path.exists(DATASET_PATH):
        print(f"Dataset found at: {DATASET_PATH}")
        train_and_save_models(DATASET_PATH)

        result = predict_property(
            type_="Flat",  # This will be mapped to "house_type" in the function
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
    else:
        print(f"Dataset {DATASET_PATH} not found. Please provide the dataset to train models.")