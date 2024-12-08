# DE_Final_Project

## Dataset Overview

Source: https://www.kaggle.com/datasets/goyaladi/fraud-detection-dataset/data

This  Financial Fraud Detection Dataset represents transactional data that includes information about transactions made by customers with merchants. Each row corresponds to a unique transaction, and the data includes details about the transaction, the customer, and the merchant as well as other elements. This dataset is only reelvant during the training phase of the machine learning model.  The dataset is based on real-world data. 

Key points:

- Unique Identifier: Each transaction is uniquely identified by `TransactionID`

- Many-to-Many Relationship:
Customer and Merchant: Customers and merchants can appear multiple times due to multiple transactions.
One customer (CustomerID) can make multiple transactions with the same or different merchants.
One merchant (MerchantID) can process transactions from multiple customers.


## Column Explanation

`TransactionID`:
- Unique identifier for each transaction.
- Ensures that no two transactions share the same ID.

`Timestamp`:
- The date and time the transaction occurred.
- Useful for time-based analysis, such as trends or transaction frequency.

`MerchantID`:
- Unique identifier for merchants.
- Multiple rows can have the same MerchantID because a merchant can process multiple transactions.

`Amount`:
- The monetary value of the transaction.
- Represents how much was spent in that specific transaction.

`CustomerID`:
- Unique identifier for customers.
- A single customer can make multiple transactions, so CustomerID is repeated.

`TransactionAmount`:
- The total amount processed for the transaction.
- Might be used in analysis of spending habits.

`AnomalyScore`:
- A numerical score indicating the likelihood of the transaction being anomalous.
- Higher scores indicate higher chances of irregularities.

`FraudIndicator`:
- Binary column (0 or 1) indicating whether the transaction was flagged as fraudulent.
- 0 means non-fraudulent, 1 means fraudulent.

`Category`:
- Describes the type of transaction (e.g., Online, Food, Travel, Other).
- Helps classify transactions for segmentation.

`MerchantName`:
- Name of the merchant associated with the transaction.
- Derived from MerchantID.

`MerchantLocation`:
- Location of the merchant associated with the transaction.
- Provides geographical context for the transaction.

`CustomerName`:
- Name of the customer who made the transaction.
- Derived from CustomerID.

`CustomerAge`:
- Age of the customer at the time of the transaction.
- Useful for demographic analysis.

`CustomerAddress`:
- Address of the customer who made the transaction.
- Can be used to study geographical spending patterns.


