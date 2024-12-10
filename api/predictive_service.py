import pickle

# Load model
# TODO: check correctness of model integration
model_path = "models/ml_model.pkl"
with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)


def make_prediction(features):
    """Run the model prediction."""
    prediction = model.predict([features])
    return prediction[0]
