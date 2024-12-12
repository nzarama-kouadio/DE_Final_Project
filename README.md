# DE_Final_Project
[![apprunner](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml)
[![CICD](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml)

## Dataset Overview

Source: https://www.kaggle.com/datasets/goyaladi/fraud-detection-dataset/data

This  Financial Fraud Detection Dataset represents transactional data that includes information about transactions made by customers with merchants. Each row corresponds to a unique transaction, and the data includes details about the transaction, the customer, and the merchant as well as other elements. This dataset is only relevant during the training phase of the machine learning model. The dataset is based on real-world data. 

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

`LastLogin`:
- Date at which the account was logged into
- it could have been by the customer or an unothorized individual

`SuspiciousFlag`:
- Binary column (0 or 1) indicating whether the transaction was flaggeda as suspicious
- 0 means non-suspicious, 1 means suspicious.

## Quantitative Assessment: System Performance Assessment

This document provides a detailed quantitative assessment of the system's performance under a load test of 10,000 concurrent users. The load test highlights the system's ability to handle a high number of concurrent requests while maintaining consistent response times. Both endpoints were tested thoroughly, with `/predict` processing a larger volume of requests compared to `/health`. The results demonstrate that the system is equipped to manage significant traffic, offering insights into its current capacity and performance under load.

### Perfomance Metrics

- **Throughput**: 1,987.96 requests/sec.

This represents the total number of successful requests the system handled per second. A throughput of ~2,000 requests/sec demonstrates the system's ability to process a substantial number of requests under high load, showcasing its capacity to handle concurrent users efficiently.

- **Max Response Time**: 163,959 ms (~164 seconds).
The maximum time it took for a request to be processed. This value indicates how the system performed under peak stress when handling the most resource-intensive requests.

- **Average Response Time**: 7,148 ms (~7.1 seconds). 
The average time it took to process all requests during the test. This gives a sense of how quickly the system responds under load and is an important indicator of user experience.

- **Failure Rate**: 5.67%
This is the percentage of requests that failed during the test.
A failure rate below 10% indicates the system can manage a majority of requests successfully, even under a high load of 10,000 users.

### Endpoint-Level Results

## **Endpoint-Level Results**

| Endpoint             | Total Requests | Median Response Time | Average Response Time | Failures    |
|----------------|----------------|-----------------------|------------------------|-------------|
| **GET `/health`** | 115,383        | 790 ms                | 7,046 ms               | 5,781 (~5%) |
| **POST `/predict`** | 231,245        | 880 ms                | 7,229 ms               | 13,875 (~6%) |










