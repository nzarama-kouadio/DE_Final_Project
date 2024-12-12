# DE_Final_Project
Fraud Detection

## Modelling
#### Data Source
The raw data was consolidated from multiple .csv files into a single dataset prepared for model building:
- `account_activity.csv`
- `customer_data.csv`
- `fraud_indicators.csv`
- `suspicious_activity.csv`
- `merchant_data.csv`
- `transaction_category_labels.csv`
- `amount_data.csv`
- `anomaly_scores.csv`
- `transaction_metadata.csv`
- `transaction_records.csv`

#### Data Preparation
- Cleaned the data to ensure consistency and removed irrelevant features.
- Engineered new features to improve model performance, such as Gap, which calculates the time difference between the last login and the reported case time.
- Split the dataset into training and testing sets (e.g., 80-20 split) to ensure robust evaluation.

#### Model Selection
- Addressed class imbalance using SMOTE (Synthetic Minority Oversampling Technique) and FROST (Feature space RObust Synthetic saTuration).
- Trained and compared multiple machine learning algorithms, including:
	- Random Forest Classifier
	- Logistic Regression
	- Support Vector Machine
	- K-Nearest Neighbors
	- Gradient Boosting Classifier
	- Decision Tree Classifier
- Random Forest Classifier emerged as the best-performing model, with hyperparameters optimized using GridSearchCV.

#### Cross Validation
- Employed cross-validation to ensure that the model generalized well to unseen data.
- Assessed model performance using metrics such as accuracy, precision, recall and F1-score.
- Achieved a precision of 1.0, indicating a perfect predictive capability.

#### Final Model Integration
- The trained model was integrated into a real-time API using Flask, FastAPI.
- Deployed the API using AWS App Runner for scalability and reliability.
- Validated the API’s functionality by testing it with sample input data, confirming its ability to handle live requests seamlessly.