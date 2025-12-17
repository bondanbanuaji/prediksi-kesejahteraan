#!/usr/bin/env python3
"""
Verification script to test the saved model
"""

import joblib
import pandas as pd
import numpy as np

# Load the saved model
model_path = 'rf_model_kesejahteraan.pkl'
artifacts = joblib.load(model_path)

model = artifacts['model']
scaler = artifacts['scaler']
mapping = artifacts['mapping']
features = artifacts['features']

print("📊 VERIFICATION OF SAVED MODEL:")
print("="*50)
print(f"Model type: {type(model)}")
print(f"Scaler type: {type(scaler)}")
print(f"Mapping: {mapping}")
print(f"Features: {features}")
print(f"Number of estimators in RF: {model.n_estimators}")

# Test with sample data
sample_data = pd.DataFrame([[10000, 5000, 1000000000.0, 12.0]], columns=features)
scaled_sample = scaler.transform(sample_data)

prediction = model.predict(scaled_sample)
prediction_proba = model.predict_proba(scaled_sample)

predicted_class = mapping[int(prediction[0])]
probabilities = {mapping[i]: prob for i, prob in enumerate(prediction_proba[0])}

print("\n🧪 TEST WITH SAMPLE DATA:")
print("-"*30)
print(f"Input: {dict(zip(features, sample_data.iloc[0]))}")
print(f"Predicted class: {predicted_class}")
print(f"Prediction probabilities: {probabilities}")
print("\n✅ Model loaded and tested successfully!")