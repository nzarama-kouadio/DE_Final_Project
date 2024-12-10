from flask import Flask, jsonify, request
from ingestion_service import ingest_data
from preprocessing import preprocess_data
from feature_engineering.real_time_features import real_time_features
from predictive_service import make_prediction

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# TODO: check correctness
@app.route('/check_fraud', methods=['POST'])
# get input data, return if data is fraud
def log_data():
    try:
        raw_data = request.json
        response = ingest_data(raw_data)
        if response["status"] == "success":
            return jsonify(response), 200
        else:
            return jsonify(response), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
# call model
def predict():
    try:
        input_data = request.json
        # Step 1: Preprocess the data
        preprocessed_data = preprocess_data(input_data)
        # Step 2: Perform real-time feature engineering
        # TODO: recheck if we will have feature engineering
        features = real_time_features(preprocessed_data)
        # Step 3: Make prediction
        prediction = make_prediction(features)
        # TODO: double check that make_prediction includes explanation (SHAP) yet
        return jsonify({"prediction": prediction}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
