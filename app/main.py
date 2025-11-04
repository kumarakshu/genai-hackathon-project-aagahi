# === 1. Import Core Libraries ===
import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# === 2. Initialize Flask App ===
app = Flask(__name__)

# === 3. Load the Pre-trained Model ===
# Define the path to the saved model file.
model_path = 'dengue_risk_model.joblib'
try:
    # Load the scikit-learn model from the .joblib file.
    model = joblib.load(model_path)
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the exact feature names the model was trained on.
# The order must match the order used during training.
MODEL_FEATURES = [
    'rainfall_mm',
    'avg_temp_c',
    'water_logging_complaints',
    'waste_complaints'
]

# === 4. Health Check Route ===
# This route is essential for Vertex AI to check if the container is running.
@app.route('/')
def home():
    """A simple health check endpoint."""
    return "API is running!"

# === 5. Prediction Route ===
# This is the main endpoint that will receive prediction requests.
@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives data from Vertex AI, runs prediction, and returns the result.
    """
    if model is None:
        return jsonify({'error': 'Model is not loaded properly.'}), 500

    try:
        # Vertex AI sends prediction requests in a specific JSON format.
        # We must parse the 'instances' key, which is a list.
        json_data = request.get_json()
        data = json_data['instances'][0] # We process the first instance.

        # Create a 2D list (or DataFrame) in the correct feature order.
        input_data_list = [
            data['rainfall_mm'],
            data['avg_temp_c'],
            data['water_logging_complaints'],
            data['waste_complaints']
        ]

        # Convert the list to a Pandas DataFrame with the correct feature names.
        # This prevents the "X does not have valid feature names" warning.
        input_df = pd.DataFrame([input_data_list], columns=MODEL_FEATURES)

        # Run the prediction.
        prediction_val = model.predict(input_df)

        # Convert the numerical prediction (0 or 1) into a human-readable string.
        if prediction_val[0] == 1:
            result = "HIGH RISK"
        else:
            result = "LOW RISK"

        # Format the output as per Vertex AI requirements.
        # The response must be a JSON object with a 'predictions' key.
        output = {
            'prediction': result,
            'input_data_received': data # (Optional) Include received data for debugging.
        }

        return jsonify({"predictions": [output]})

    except KeyError as e:
        # Error if a required feature is missing from the request.
        return jsonify({'error': f'Missing key in request: {str(e)}'}), 400
    except Exception as e:
        # A general error handler for any other issues.
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

# === 6. Server Start ===
if __name__ == '__main__':
    # This block is used for local testing (e.g., `python main.py`).
    # It will NOT be executed when deployed with Gunicorn in production.
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)