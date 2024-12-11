def make_prediction(model, features):
    """
    Predict using the loaded model.

    Args:
        model: Loaded machine learning model.
        features (pd.DataFrame): Feature-engineered data.

    Returns:
        list: Model predictions for the input features.
    """
    # Perform the prediction
    predictions = model.predict(features.values).tolist()
    
    # Map numeric predictions to labels
    label_mapping = {0.0: "Not Fraud", 1.0: "Fraud"}
    return [label_mapping.get(pred, "Unknown") for pred in predictions]
