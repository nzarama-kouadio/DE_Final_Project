import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder for 'Category'
label_encoder = LabelEncoder()

def preprocess_data(input_data):
    """
    Preprocess raw input data for the model.

    Args:
        input_data (list[dict]): Raw input data from the user.

    Returns:
        pd.DataFrame: Preprocessed DataFrame ready for feature engineering.
    """
    try:
        # Convert input JSON data to a DataFrame
        if isinstance(input_data, dict):  # Single record case
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, list):  # Multiple records case
            df = pd.DataFrame(input_data)
        else:
            raise ValueError("Input data must be a dict or a list of dicts.")

        # Validate required columns
        required_columns = [
            "TransactionID", "Timestamp", "MerchantID", "Amount", "CustomerID",
            "TransactionAmount", "AnomalyScore", "Category", "CustomerAge",
            "AccountBalance", "SuspiciousFlag", "LastLogin"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Convert datetime columns
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["LastLogin"] = pd.to_datetime(df["LastLogin"])

        # Encode categorical columns
        df["Category"] = label_encoder.fit_transform(df["Category"])

        # Drop unnecessary columns
        columns_to_drop = ["TransactionID", "MerchantID", "CustomerID"]
        df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

        # Handle missing values
        df.fillna(0, inplace=True)

        return df

    except Exception as e:
        raise ValueError(f"Error during preprocessing: {e}")
