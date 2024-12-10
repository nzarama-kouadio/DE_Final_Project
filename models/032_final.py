"""
Data Modelling
"""

# importing the required libraries
import pandas as pd
import numpy as np
import pickle

# Preprocessing
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Model Selection and Cross-Validation
from sklearn.model_selection import (
    train_test_split,
    KFold,
    cross_val_score,
    GridSearchCV,
)

# Machine Learning Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

# Metrics
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Imbalanced Data Handling
from imblearn.over_sampling import SMOTE

fraud = pd.read_csv("complete_dataset.csv")
print(fraud.columns)

columns_to_be_dropped = [
    "TransactionID",
    "MerchantID",
    "CustomerID",
    "CustomerName",
    "MerchantName",
    "MerchantLocation",
    "CustomerAddress",
]

# dropping the columns that are not needed
fraud1 = fraud.drop(columns_to_be_dropped, axis=1)

fraud1["FraudIndicator"].value_counts()
"""This dataset is very imbalanced as the number of cases which are fraudulent are very few. 
Thus, the models would not be able to predict these cases very accurately.
"""

# FEATURE ENGINEERING

# converting the TimeStamp to a datetime format
fraud1["Timestamp"] = pd.to_datetime(fraud1["Timestamp"])
print(fraud1.dtypes)

# Extract useful time-based features
fraud1["Hour"] = fraud1["Timestamp"].dt.hour
fraud1["Day"] = fraud1["Timestamp"].dt.day
fraud1["Month"] = fraud1["Timestamp"].dt.month
fraud1["Weekday"] = fraud1["Timestamp"].dt.weekday
fraud1["Year"] = fraud1["Timestamp"].dt.year

X = fraud1.drop(["FraudIndicator", "Timestamp"], axis=1)
y = fraud1["FraudIndicator"]

# initializing LabelEncoder
label_encoder = LabelEncoder()

# fit and transform the Category column
X["Category"] = label_encoder.fit_transform(X["Category"])
X.head(10)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# checking the sizes
X_train.shape, y_test.shape

# LOGISTIC REGRESSION MODEL
log_mod = LogisticRegression()

log_mod.fit(X_train, y_train)

y_pred = log_mod.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale the features to [0, 1] range
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Apply SMOTE for oversampling
smote = SMOTE()
X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)


# Define FROST function
def generate_frost_samples(X_minority, initial_feature_index, k=5, m=1.5):
    initial_feature_values = X_minority[:, initial_feature_index]
    similarity_matrix = 1 / (
        1 + np.abs(initial_feature_values[:, np.newaxis] - initial_feature_values)
    )
    k_nearest_indices = np.argsort(similarity_matrix, axis=1)[:, -k:]
    synthetic_samples_initial = []
    for i in range(len(initial_feature_values)):
        for j in k_nearest_indices[i]:
            synthetic_value = initial_feature_values[i] + m * (
                initial_feature_values[j] - initial_feature_values[i]
            )
            synthetic_sample = np.copy(X_minority[i])
            synthetic_sample[initial_feature_index] = synthetic_value
            synthetic_samples_initial.append(synthetic_sample)
    return np.array(synthetic_samples_initial)


# Apply FROST for oversampling
initial_feature_index = 0  # Choose the index of the initial feature to oversample
X_train_frost = generate_frost_samples(
    X_train_scaled[y_train == 1], initial_feature_index, k=5, m=1.5
)

# Combine original and synthetic samples
X_train_combined = np.vstack((X_train_scaled, X_train_frost))
y_train_combined = np.concatenate((y_train, np.ones(len(X_train_frost))))

# Initialize the Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

# Define the number of folds for k-fold cross-validation
k_folds = KFold(n_splits=5)

# Perform cross-validation and calculate the scores for SMOTE
scores_smote = cross_val_score(clf, X_train_smote, y_train_smote, cv=k_folds)

# Perform cross-validation and calculate the scores for FROST
scores_frost = cross_val_score(clf, X_train_combined, y_train_combined, cv=k_folds)

# Print the cross-validation scores for each fold
print("SMOTE Cross Validation Scores: ", scores_smote)
print("FROST Cross Validation Scores: ", scores_frost)

# Print the average cross-validation score
print("Average SMOTE CV Score: ", scores_smote.mean())
print("Average FROST CV Score: ", scores_frost.mean())

# FROST gives a higher score

# LOGISTIC REGRESSION
log_mod = LogisticRegression()

log_mod.fit(X_train_smote, y_train_smote)
log_mod.fit(X_train_combined, y_train_combined)

y_predSMOTE = log_mod.predict(X_test)
y_predFROST = log_mod.predict(X_test)

print("Model Evaluation Metrics: SMOTE")
print(classification_report(y_test, y_predSMOTE))
print(confusion_matrix(y_test, y_predSMOTE))

print("\nModel Evaluation Metrics: FROST")
print(classification_report(y_test, y_predFROST))
print(confusion_matrix(y_test, y_predFROST))

# HYPERPARAMETER TUNING WITH SMOTE
# Define a range of hyperparameters to search
param_grid = {
    "penalty": ["l1", "l2"],  # Regularization type
    "C": np.logspace(
        -3, 3, 7
    ),  # Inverse of regularization strength (smaller values for stronger regularization)
    "solver": ["liblinear"],  # Solver for l1 regularization
}

# Create a grid search with cross-validation
grid_search = GridSearchCV(log_mod, param_grid, cv=5, scoring="f1", n_jobs=-1)

# Fit the grid search to the data
grid_search.fit(X_train_smote, y_train_smote)

# Get the best hyperparameters and corresponding model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Print the best hyperparameters
print("Best Hyperparameters:", best_params)

# Evaluate the best model on the resampled data
y_pred = best_model.predict(X_train_smote)

print("Model Evaluation Metrics on Resampled Data- SMOTE:")
print(classification_report(y_train_smote, y_pred))
print(confusion_matrix(y_train_smote, y_pred))

# HYPERPARAMETER TUNING WITH FROST
# Define a range of hyperparameters to search
param_grid = {
    "penalty": ["l1", "l2"],  # Regularization type
    "C": np.logspace(
        -3, 3, 7
    ),  # Inverse of regularization strength (smaller values for stronger regularization)
    "solver": ["liblinear"],  # Solver for l1 regularization
}

# Create a grid search with cross-validation
grid_search = GridSearchCV(log_mod, param_grid, cv=5, scoring="f1", n_jobs=-1)

# Fit the grid search to the data
grid_search.fit(X_train_combined, y_train_combined)

# Get the best hyperparameters and corresponding model
best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Print the best hyperparameters
print("Best Hyperparameters:", best_params)

# Evaluate the best model on the resampled data
y_pred = best_model.predict(X_train_combined)

print("Model Evaluation Metrics on Resampled Data- FROST:")
print(classification_report(y_train_combined, y_pred))
print(confusion_matrix(y_train_combined, y_pred))


# EVALUATING WITH SMOTE FOR DIFFERENT CLASSIFIERS
def evaluate_classification_models(X_train_smote, y_train_smote):
    # Split the resampled data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_train_smote, y_train_smote, test_size=0.2, random_state=42
    )

    # Define a dictionary of classification models
    models = {
        "Decision Tree Classifier": DecisionTreeClassifier(),
        "Random Forest Classifier": RandomForestClassifier(),
        "Support Vector Machine (SVM)": SVC(),
        "K-Nearest Neighbors (KNN)": KNeighborsClassifier(),
        "Gradient Boosting Classifier": GradientBoostingClassifier(),
    }

    results = {}

    for model_name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate and store various metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)

        results[model_name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "Confusion Matrix": confusion,
        }

    return results


results = evaluate_classification_models(X_train_smote, y_train_smote)
for model_name, model_result in results.items():
    print(f"Results for {model_name}:")
    for metric, value in model_result.items():
        print(f"{metric}: {value}")
    print()


# EVALUATING WITH FROST FOR DIFFERENT CLASSIFIERS
def evaluate_classification_models(X_train_combined, y_train_combined):
    # Split the resampled data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_train_combined, y_train_combined, test_size=0.2, random_state=42
    )

    # Define a dictionary of classification models
    models = {
        "Decision Tree Classifier": DecisionTreeClassifier(),
        "Random Forest Classifier": RandomForestClassifier(),
        "Support Vector Machine (SVM)": SVC(),
        "K-Nearest Neighbors (KNN)": KNeighborsClassifier(),
        "Gradient Boosting Classifier": GradientBoostingClassifier(),
    }

    results = {}

    for model_name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate and store various metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        confusion = confusion_matrix(y_test, y_pred)

        results[model_name] = {
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
            "Confusion Matrix": confusion,
        }

    return results


results = evaluate_classification_models(X_train_combined, y_train_combined)
for model_name, model_result in results.items():
    print(f"Results for {model_name}:")
    for metric, value in model_result.items():
        print(f"{metric}: {value}")
    print()

"""
After the evaluation, the ranking of the classifiers is as follows:
1. Random Forest Classifier
2. Gradient Boosting Algorithm
3. Decision Tree Classifier
4. K-Nearest Neighbors
5. Support Vector Machine
6. Logistic Regression
"""

# HYPERPARAMETER TUNING FOR RANDOM FOREST
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_train_combined, y_train_combined, test_size=0.2, random_state=42
)

# Define the Random Forest Classifier model
rf_model = RandomForestClassifier(random_state=42)

# Define a range of hyperparameters to search
param_grid = {
    "n_estimators": [50, 100, 150],  # Number of trees in the forest
    "max_depth": [None, 10, 20, 30],  # Maximum depth of the trees
    "min_samples_split": [
        2,
        5,
        10,
    ],  # Minimum number of samples required to split an internal node
    "min_samples_leaf": [
        1,
        2,
        4,
    ],  # Minimum number of samples required to be at a leaf node
}

# Create a grid search with cross-validation
grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring="f1", n_jobs=-1)

# Fit the grid search to the resampled data
grid_search.fit(X_train, y_train)

# Get the best hyperparameters and corresponding model
best_params = grid_search.best_params_
best_rf_model = grid_search.best_estimator_

# Print the best hyperparameters
print("Best Hyperparameters:", best_params)

# Train the best model on the training data
best_rf_model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = best_rf_model.predict(X_test)

# Calculate and print various metrics to evaluate the best model's performance
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)

print("Best Model Evaluation Metrics:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:")
print(confusion)

# saving it as a .pkl file

with open("ml_model.pkl", "wb") as file:
    pickle.dump(best_rf_model, file)

print("Model saved as 'ml_model.pkl'")
