from flask import Flask, jsonify, request
from api.preprocessing_service import preprocess_data
from api.predictive_service import make_prediction
from api.explanation_service import generate_cache_shap_explanations
from api.feature_engineering_service import perform_feature_engineering
import pickle

# Load model once to improve performance
def load_model(model_path="models/ml_model.pkl"):
    with open(model_path, "rb") as model_file:
        return pickle.load(model_file)

ml_model = load_model()

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({"status": "healthy"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict fraud and provide SHAP explanations.
    """
    try:
        input_data = request.json
        if not input_data:
            return jsonify({"error": "Invalid input data"}), 400
        
        # Step 1: Preprocess the data
        preprocessed_data = preprocess_data(input_data)

        # Step 2: Perform real-time feature engineering
        features = perform_feature_engineering(preprocessed_data)

        # Step 3: Make prediction using the pre-loaded model
        prediction = make_prediction(ml_model, features)

        # Step 4: Generate SHAP explanations
        features_tuple = tuple(map(tuple, features.values))
        plot_urls = generate_cache_shap_explanations(ml_model, features_tuple)

        # Return the prediction in JSON and display the HTML
        return jsonify({
            "prediction": prediction,
            "plot_urls": plot_urls
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
