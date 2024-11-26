import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from django.conf import settings
import joblib
import os
import numpy as np

class StudentPerformancePredictor:
    def __init__(self):
        self.model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'student_performance.joblib')
        self.scaler_path = os.path.join(settings.BASE_DIR, 'ml_models', 'scaler.joblib')
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """Load the trained model and scaler if they exist"""
        try:
            self.model = joblib.load(self.model_path)
            self.scaler = joblib.load(self.scaler_path)
        except FileNotFoundError:
            self.model = RandomForestRegressor()
            self.scaler = StandardScaler()

    def train_model(self, features, targets):
        """Train the model with new data"""
        scaled_features = self.scaler.fit_transform(features)
        self.model.fit(scaled_features, targets)
        
        # Save the trained model and scaler
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

    def predict(self, features):
        """Make predictions using the trained model"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        scaled_features = self.scaler.transform(features)
        return self.model.predict(scaled_features)

def train_model(data):
    # Prepare the data
    X = data.drop('score', axis=1)
    y = data['score']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # Save the model and scaler
    model_path = os.path.join(settings.BASE_DIR, 'ml_ops', 'models')
    os.makedirs(model_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_path, 'student_prediction_model.joblib'))
    joblib.dump(scaler, os.path.join(model_path, 'student_prediction_scaler.joblib'))

    return model, scaler

def predict_score(student_data):
    model_path = os.path.join(settings.BASE_DIR, 'ml_ops', 'models')
    model = joblib.load(os.path.join(model_path, 'student_prediction_model.joblib'))
    scaler = joblib.load(os.path.join(model_path, 'student_prediction_scaler.joblib'))

    # Prepare the input data
    X = pd.DataFrame([student_data])
    X_scaled = scaler.transform(X)

    # Make prediction
    prediction = model.predict(X_scaled)

    return prediction[0]

