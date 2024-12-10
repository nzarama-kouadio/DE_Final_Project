from flask import jsonify
# TODO: design how our app will take input and what columns do we need
# suggestion make user input all columns in the final merged df
# TODO: test with mock input data
# we can use the compelte_dataset first to make sure that our app handle properly
def ingest_data(raw_data):
    """Ingest raw transaction data."""
    try:
        # Validate the input structure
        if not isinstance(raw_data, dict):
            raise ValueError("Input data must be a JSON object.")

        # Check required fields
        required_fields = ["transaction_id", "amount", "timestamp", "merchant"]
        for field in required_fields:
            if field not in raw_data:
                raise ValueError(f"Missing required field: {field}")

        # Simulate ingestion success
        response = {
            "status": "success",
            "message": "Data ingested successfully.",
            "data": raw_data
        }
        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
