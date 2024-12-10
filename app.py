from flask import Flask, jsonify, request
from api.preprocessing import preprocess_data
from api.predictive_service import make_prediction
from api.explanation_service import generate_shap_explanations
from feature_engineering.real_time_features import real_time_features
import pickle

# Load the trained model once at startup
MODEL_PATH = "models/ml_model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        ml_model = pickle.load(f)  # Load the model into memory
except FileNotFoundError:
    raise FileNotFoundError(f"Default model not found at {MODEL_PATH}")

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json
        if not input_data:
            return jsonify({"error": "Invalid input data"}), 400
        
        # Step 1: Preprocess the data
        preprocessed_data = preprocess_data(input_data)

        # Step 2: Perform real-time feature engineering
        # TODO: recheck if we will have feature engineering
        features = real_time_features(preprocessed_data)

        # Step 3: Make prediction using the pre-loaded model
        prediction = make_prediction(ml_model, features)

        # Step 4: Generate SHAP explanations
        shap_values, plot_paths = generate_shap_explanations(ml_model, features)

        # Return prediction and explanation
        return jsonify({
            "prediction": prediction,
            "explanation": shap_values.tolist(),
            "bar_plot_path": plot_paths.get("bar_plot"),
            "summary_plot_path": plot_paths.get("summary_plot"),
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
