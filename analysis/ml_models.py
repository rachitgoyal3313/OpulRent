import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn. model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Paths
MODEL_PATH = "property_price_model_india.joblib"

# Sample training data generation (for MVP)
def generate_sample_data():
    np.random.seed(42)
    data = {
        'area_sqft': np.random.randint(500, 2500, 100),
        'bedrooms': np.random.randint(1, 5, 100),
        'bathrooms': np.random.randint(1, 4, 100),
        'location': np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Pune'], 100),
        'property_type': np.random.choice(['apartment', 'house', 'commercial'], 100)
    }

    df = pd.DataFrame(data)

    df['price'] = (
        df['area_sqft'] * 5000 +
        df['bedrooms'] * 200000 +
        df['bathrooms'] * 150000 +
        df['location'].map({
            'Mumbai': 1000000,
            'Delhi': 800000,
            'Bangalore': 900000,
            'Hyderabad': 700000,
            'Pune': 850000
        }) +
        df['property_type'].map({
            'apartment': 100000,
            'house': 200000,
            'commercial': 300000
        }) +
        np.random.randint(-100000, 100000, 100)
    )

    return df

# Training and saving the model
def train_and_save_model():
    df = generate_sample_data()
    X = df[['area_sqft', 'bedrooms', 'bathrooms', 'location', 'property_type']]
    y = df['price']

    categorical_features = ['location', 'property_type']

    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ], remainder='passthrough')

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)

# Load model from file or train if not exists
def load_model():
    if not os.path.exists(MODEL_PATH):
        train_and_save_model()
    return joblib.load(MODEL_PATH)

# Prediction logic
def predict_property_metrics(area_sqft, bedrooms, bathrooms, location, property_type):
    model = load_model()

    input_df = pd.DataFrame([{
        'area_sqft': area_sqft,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'location': location,
        'property_type': property_type
    }])

    predicted_price = model.predict(input_df)[0]

    # Growth score and rent/ROI calculations
    location_growth_map = {
        'Mumbai': 8.5,
        'Delhi': 7.5,
        'Bangalore': 9.0,
        'Hyderabad': 8.2,
        'Pune': 8.0
    }

    location_rent_factor = {
        'Mumbai': 0.008,
        'Delhi': 0.0075,
        'Bangalore': 0.0085,
        'Hyderabad': 0.007,
        'Pune': 0.0078
    }

    property_expense_map = {
        'apartment': 0.35,
        'house': 0.4,
        'commercial': 0.3
    }

    rental_factor = location_rent_factor.get(location, 0.0075)
    expense_ratio = property_expense_map.get(property_type.lower(), 0.35)
    growth = location_growth_map.get(location, 7.0)

    monthly_rent = predicted_price * rental_factor
    annual_rent = monthly_rent * 12
    annual_expenses = annual_rent * expense_ratio
    net_income = annual_rent - annual_expenses
    roi = (net_income / predicted_price) * 100

    return {
        "predicted_price_inr": round(predicted_price),
        "monthly_rent_inr": round(monthly_rent),
        "roi_percent": round(roi, 2),
        "growth_score_out_of_10": growth
    }

# Test run
if __name__ == "__main__":
    result = predict_property_metrics(
        area_sqft=1500,
        bedrooms=3,
        bathrooms=2,
        location="Bangalore",
        property_type="apartment"
    )
    print(result)