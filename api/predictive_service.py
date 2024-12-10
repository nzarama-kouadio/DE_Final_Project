# Load model
# TODO: check correctness of model integration
def make_prediction(model, features):
    """Run the model prediction."""
    prediction = model.predict([features])
    return prediction[0]
