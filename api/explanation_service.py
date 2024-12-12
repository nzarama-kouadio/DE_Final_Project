import shap
import matplotlib.pyplot as plt
import os
import uuid
from functools import lru_cache
import pandas as pd


@lru_cache(maxsize=100)
def generate_cache_shap_explanations(model, features_tuple):
    features = pd.DataFrame(features_tuple)
    return generate_shap_explanations(model, features)

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

        return shap_values_class1, plot_paths

    except Exception as e:
        raise ValueError(f"Error generating SHAP explanations: {e}")
