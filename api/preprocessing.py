import pandas as pd

# TODO: check code (how to clean data)
def validate_input(data):
    """Validate raw input data."""
    # Example validation: Check required keys
    required_keys = ["transaction_id", "amount", "timestamp"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")

    return True

def clean_data(data):
    """Clean and standardize input data."""
    # Standardize timestamp format
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    return data

def preprocess_data(raw_data):
    """High-level preprocessing function."""
    validate_input(raw_data)
    cleaned_data = clean_data(raw_data)
    return cleaned_data
