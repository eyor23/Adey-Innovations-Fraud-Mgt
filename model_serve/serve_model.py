from flask import Flask, request, jsonify
import joblib
import logging
import numpy as np

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your pre-trained model
model = joblib.load(r'C:\Users\user\Desktop\Kifiya\fraud_model.joblib')

@app.route('/')
def home():
    return {"message": "Welcome to the Fraud Detection API"}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input features from the request
        features = request.json

        # Convert feature values to standard Python floats
        feature_values = np.array([
            features['purchase_value'],
            features['age'],
            features['ip_address'],
            features['signup_hour'],
            features['signup_day_of_week'],
            features['purchase_hour'],
            features['purchase_day_of_week'],
            features['purchase_frequency_proxy'],
            features['source_Direct_False'],
            features['source_Direct_True'],
            features['source_SEO_False'],
            features['source_SEO_True'],
            features['browser_FireFox_False'],
            features['browser_FireFox_True'],
            features['browser_IE_False'],
            features['browser_IE_True'],
            features['browser_Safari_False'],
            features['browser_Safari_True'],
            features['browser_Opera_False'],
            features['browser_Opera_True'],
            features['sex_0'],
            features['sex_1']
        ]).astype(float)  # Convert to standard Python float

        # Log the feature values and their data types
        logger.info(f"Feature values: {feature_values}")
        logger.info(f"Feature types: {[type(value).__name__ for value in feature_values]}")

        # Make prediction
        prediction = model.predict([feature_values])

        logger.info(f"Prediction: {prediction[0]}")

        return jsonify({"prediction": prediction[0]})
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
