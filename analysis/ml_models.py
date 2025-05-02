import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# File path to your Excel data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'cities_with_varied_estimated_prices.xlsx')

# Growth scores by city
CITY_GROWTH_SCORES = {
    'Mumbai': 9.0,
    'Pune': 8.5,
    'Nagpur': 7.0,
    'Bangalore': 9.5,
    'New Delhi': 8.0
}

# Load and preprocess data
def load_data():
    df = pd.read_excel(DATA_PATH)

    feature_columns = [
        'locality', 'city', 'area', 'Estimated Price', 'beds',
        'bathrooms', 'type', 'furnishing'
    ]
    target_columns = ['rent', 'Rental Yield (%)']

    df = df.dropna(subset=feature_columns + target_columns)

    return df, feature_columns, target_columns

# Train model
def train_model():
    df, feature_columns, target_columns = load_data()

    X = df[feature_columns]
    y = df[target_columns]

    categorical_features = ['locality', 'city', 'type', 'furnishing']
    numerical_features = ['area', 'Estimated Price', 'beds', 'bathrooms']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model.fit(X_train, y_train)

    # Save model to file (optional)
    joblib.dump(model, os.path.join(BASE_DIR, 'trained_model.pkl'))

    return model

# Load model (use cached if available)
def get_model():
    model_path = os.path.join(BASE_DIR, 'trained_model.pkl')
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return train_model()

# Compute growth score from city
def compute_growth_score(city):
    return CITY_GROWTH_SCORES.get(city, 6.0)

# Predict function callable from Django views
def predict_rent_roi_growth(user_input):
    model = get_model()
    input_df = pd.DataFrame([user_input])
    prediction = model.predict(input_df)

    predicted_rent = prediction[0][0]
    predicted_roi = prediction[0][1]
    predicted_growth = compute_growth_score(user_input['city'])

    return {
        'predicted_rent': round(predicted_rent),
        'predicted_roi': round(predicted_roi, 2),
        'growth_score': predicted_growth
    }