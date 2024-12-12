import os
import uuid
from functools import lru_cache
import pandas as pd
import boto3
import shap
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
bucket_name = os.getenv("S3_BUCKET_NAME")

# Initialize the S3 client using the loaded environment variables
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION"),
)

@lru_cache(maxsize=100)
def generate_cache_shap_explanations(model, features_tuple):
    features = pd.DataFrame(features_tuple)
    return generate_shap_explanations(model, features)

def upload_to_s3(file_path, s3_key):
    try:
        # Upload file to S3
        s3.upload_file(file_path, bucket_name, s3_key)
        # Generate a pre-signed URL
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": s3_key},
            ExpiresIn=600,  # Time in seconds
        )
        return url
    except boto3.exceptions.S3UploadFailedError as e:
        raise ValueError(f"S3 upload failed: {e}")

def generate_shap_explanations(model, features, save_plots=True):
    """
    Generate SHAP explanations for given features using the provided model.

    Args:
        model: The trained machine learning model (compatible with SHAP).
        features: The preprocessed features for which
                  explanations are generated (Pandas DataFrame).
        save_plots: Whether to save SHAP summary plots as static files.

    Returns:
        shap_values: The computed SHAP values.
        plot_paths: A dictionary containing file paths to saved SHAP plots.
    """
    try:
        os.makedirs("static", exist_ok=True)

        # Create SHAP explainer
        explainer = shap.TreeExplainer(model)

        # Compute SHAP values
        features.columns = ['Amount', 'TransactionAmount', 'AnomalyScore', 'Category',
                            'CustomerAge', 'AccountBalance', 'SuspiciousFlag', 'gap', 
                            'Hour', 'Day', 'Month', 'Weekday', 'Year']
        shap_values = explainer.shap_values(features)

        # Extract SHAP values
        shap_values_class1 = shap_values[:, :, 1]

        # Generate unique filenames for plots
        unique_id = str(uuid.uuid4())
        plot_paths = {
            "bar_plot": os.path.join("static", f"shap_summary_bar_{unique_id}.png"),
            "summary_plot": os.path.join("static", f"shap_summary_{unique_id}.png"),
        }

        if save_plots:
            # Generate the bar summary plot
            shap.summary_plot(shap_values_class1, features, plot_type="bar", show=False)
            plt.savefig(plot_paths["bar_plot"])
            plt.close()

            # Generate the standard summary plot
            shap.summary_plot(shap_values_class1, features, show=False)
            plt.savefig(plot_paths["summary_plot"])
            plt.close()

        # Upload plots to S3 with unique keys
        plot_urls = {
            "bar_plot": upload_to_s3(plot_paths["bar_plot"], f"shap_summary_bar_{unique_id}.png"),
            "summary_plot": upload_to_s3(plot_paths["summary_plot"], f"shap_summary_{unique_id}.png")
        }

        # Clean up local plot files
        os.remove(plot_paths["bar_plot"])
        os.remove(plot_paths["summary_plot"])

        return plot_urls

    except Exception as e:
        raise ValueError(f"Error generating SHAP explanations: {e}")
