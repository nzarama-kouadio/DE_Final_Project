import shap
import matplotlib.pyplot as plt

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

    # Generate and save SHAP plots
    plot_paths = {
        "bar_plot": "static/shap_summary_bar.png",
        "summary_plot": "static/shap_summary.png"
    }
    if save_plots:
            # Generate the bar summary plot
            shap.summary_plot(shap_values, features, plot_type="bar", show=False)
            plt.savefig(plot_paths["bar_plot"])
            plt.close()

            # Generate the standard summary plot
            shap.summary_plot(shap_values, features, show=False)
            plt.savefig(plot_paths["summary_plot"])
            plt.close()

    return shap_values, plot_paths
