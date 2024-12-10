# TODO: confirm with Micha that we don't perform transformation, so we can skip this
def calculate_time_features(data):
    """Extract time-based features from timestamps."""
    data["hour"] = data["timestamp"].dt.hour
    data["day_of_week"] = data["timestamp"].dt.dayofweek
    return data


def encode_categorical_features(data):
    """Encode categorical variables."""
    data["merchant_encoded"] = data["merchant"].astype("category").cat.codes
    return data


def real_time_features(data):
    """End-to-end feature engineering pipeline."""
    data = calculate_time_features(data)
    data = encode_categorical_features(data)
    return data
