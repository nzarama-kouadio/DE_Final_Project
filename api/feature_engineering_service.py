def perform_feature_engineering(df):
    """
    Perform feature engineering on the preprocessed DataFrame.

    Args:
        df (pd.DataFrame): Preprocessed DataFrame.

    Returns:
        pd.DataFrame: DataFrame with engineered features.
    """
    try:
        # Calculate gap in days between Timestamp and LastLogin
        df["gap"] = (df["Timestamp"] - df["LastLogin"]).dt.days.abs()

        # Extract useful time-based features
        df["Hour"] = df["Timestamp"].dt.hour
        df["Day"] = df["Timestamp"].dt.day
        df["Month"] = df["Timestamp"].dt.month
        df["Weekday"] = df["Timestamp"].dt.weekday
        df["Year"] = df["Timestamp"].dt.year

        # Drop original datetime columns
        df.drop(columns=["Timestamp", "LastLogin"], inplace=True)

        return df

    except Exception as e:
        raise ValueError(f"Error during feature engineering: {e}")
