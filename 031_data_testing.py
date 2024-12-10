"""
Testing the data to see if everything is in place for modelling
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option("mode.copy_on_write", True)

fraud = pd.read_csv("complete_dataset.csv")

# finding the count of NA's in each column, if any
na_counts = fraud.isna().sum()
print(na_counts)

class_counts = fraud["FraudIndicator"].value_counts()
print("Value counts for the Fraud Indicator variable are as follows:")
print(class_counts)

class_proportions = fraud["FraudIndicator"].value_counts(normalize=True) * 100
print("\nClass Proportions (%):")
print(class_proportions)

print(f"Dataset contains {fraud.shape[0]} rows and {fraud.shape[1]} columns.")

print("Data types of each column:")
print(fraud.dtypes)

# Summary statistics for numerical columns
print("Statistical Summary for Numerical Columns:")
print(fraud.describe())

# Summary statistics for categorical columns
print("Unique values in categorical columns:")
categorical_cols = fraud.select_dtypes(include=["object", "category"]).columns
for col in categorical_cols:
    print(f"{col}: {fraud[col].nunique()} unique values")

selected_columns = ["CustomerAge", "TransactionAmount", "AnomalyScore", "Amount"]

# Ensure the selected columns exist in the DataFrame
numeric_cols = fraud[selected_columns]

numeric_cols.hist(bins=20, figsize=(15, 10), color="green", edgecolor="black")
plt.suptitle("Distribution of Numerical Features")
plt.show()

# Countplot for FraudIndicator
sns.countplot(x="FraudIndicator", data=fraud)
plt.title("Fraud Indicator Counts")
plt.show()

# Boxplots for numerical columns by FraudIndicator
for col in numeric_cols:
    sns.boxplot(x="FraudIndicator", y=col, data=fraud)
    plt.title(f"{col} by Fraud Indicator")
    plt.show()

# Correlation heatmap
correlation_matrix = numeric_cols.corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()
