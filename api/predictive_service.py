def make_prediction(model, features):
    """
    Predict using the loaded model.

    Args:
        model: Loaded machine learning model.
        features (pd.DataFrame): Feature-engineered data.

    Returns:
        list: Model predictions for the input features.
    """
    return model.predict(features).tolist()
