import os
import shap
import matplotlib.pyplot as plt

# Ensure SHAP library can find a display backend
os.environ["DISPLAY"] = ":0"


def generate_shap_explanations(model, features, save_plots=True):
    """
    Generate SHAP explanations for given features using the provided model.

    Args:
        model: The trained machine learning model (compatible with SHAP).
               If None, the default model will be loaded.
        features: The preprocessed features for which
                explanations are generated (Pandas DataFrame).
        save_plots: Whether to save SHAP summary plots as static files.

    Returns:
        shap_values: The computed SHAP values.
        plot_paths: A dictionary containing file paths to saved SHAP plots.
    """
    # Create SHAP explainer
    explainer = shap.TreeExplainer(model)

    # Compute SHAP values
    shap_values = explainer.shap_values(features)

    plot_paths = {}
    if save_plots:
        # Generate summary bar plot
        shap.summary_plot(shap_values, features, show=False, plot_type="bar")
        bar_plot_path = "static/shap_summary_bar.png"
        plt.savefig(bar_plot_path)
        plot_paths["bar_plot"] = f"/{bar_plot_path}"

        # Generate detailed summary plot
        shap.summary_plot(shap_values, features, show=False)
        summary_plot_path = "static/shap_summary.png"
        plt.savefig(summary_plot_path)
        plot_paths["summary_plot"] = f"/{summary_plot_path}"

    return shap_values, plot_paths
