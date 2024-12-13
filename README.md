# DE_Final_Project

[![apprunner](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml) [![CICD](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml)

## Project Goal

The goal of this project is to design and deploy a scalable microservice for real-time transaction fraud detection. The microservice integrates a machine learning model trained to identify fraudulent transactions and utilizes modern best practices, including containerization with a Distroless Docker image, feature engineering for real-time data processing, and robust Infrastructure as Code (IaC) tools for deployment. It is optimized to handle high-performance workloads, processing up to 10,000 requests per second, with reliability validated through extensive load testing and performance metrics. By combining data engineering techniques, explainability tools (e.g., SHAP), and CI/CD pipelines, this project aims to deliver a reliable and interpretable fraud detection solution while fostering collaboration and leveraging AI Pair Programming tools to enhance development efficiency.

## Project Structure

```

├── .devcontainer/          # Configuration for development environment
├── .github/workflows/      # GitHub Actions workflows for CI/CD
├── api/                    # API implementation (e.g., Flask-based services)
├── build/                  # Infrastructure setup files
├── catboost_info/          # Additional models and logs for CatBoost
├── feature_engineering/    # Feature engineering scripts and utilities
├── models/                 # Machine learning models and explainability tools
├── templates/              # Templates for workflows and visualizations
├── tests/                  # Unit and integration tests
├── Dockerfile              # Docker configuration for containerizing the app
├── Makefile                # Commands for setup, testing, and deployment
├── README.md               # Project overview and instructions
├── Team_Reflection.pdf     # Team reflection and peer evaluations
├── app.py                  # Main application file
├── assessment.py           # Quantitative assessment script
├── complete_dataset.csv    # Processed dataset
├── locust_results_stats.csv# Results from load testing
├── locustfile.py           # Load testing configuration
├── requirements.txt        # Python dependencies
├── shap_summary.png        # Visualization of SHAP summary
├── shap_summary_bar.png    # Bar chart of SHAP importance

```

## Dataset Overview

Source: https://www.kaggle.com/datasets/goyaladi/fraud-detection-dataset/data

This Financial Fraud Detection Dataset represents transactional data that includes information about transactions made by customers with merchants. Each row corresponds to a unique transaction, and the data includes details about the transaction, the customer, and the merchant as well as other elements such as fraud indicators. This dataset is only reelvant during the training phase of the machine learning model. The dataset is based on real-world data.

## Architectural Diagram
![Architectural diagram](https://github.com/user-attachments/assets/fe487cce-7782-4363-9b23-d67be194e7ee)

## Quantitative Assessment: System Performance Assessment

This document provides a detailed quantitative assessment of the system's performance under a load test of 10,000 concurrent users. The load test highlights the system's ability to handle a high number of concurrent requests while maintaining consistent response times. Both endpoints were tested thoroughly, with `/predict` processing a larger volume of requests compared to `/health`. The results demonstrate that the system is equipped to manage significant traffic, offering insights into its current capacity and performance under load.

### Perfomance Metrics

-   **Throughput**: 1,987.96 requests/sec. This represents the total number of successful requests the system handled per second. A throughput of \~2,000 requests/sec demonstrates the system's ability to process a substantial number of requests under high load, showcasing its capacity to handle concurrent users efficiently.

-   **Max Response Time**: 163,959 ms (\~164 seconds). The maximum time it took for a request to be processed. This value indicates how the system performed under peak stress when handling the most resource-intensive requests.

-   **Average Response Time**: 7,148 ms (\~7.1 seconds). The average time it took to process all requests during the test. This gives a sense of how quickly the system responds under load and is an important indicator of user experience.

-   **Failure Rate**: 5.67% This is the percentage of requests that failed during the test. A failure rate below 10% indicates the system can manage a majority of requests successfully, even under a high load of 10,000 users.

### Endpoint-Level Results

| Endpoint | Total Requests | Median Response Time | Average Response Time | Failures |
|---------------|---------------|---------------|---------------|---------------|
| **GET `/health`** | 115,383 | 790 ms | 7,046 ms | 5,781 (\~5%) |
| **POST `/predict`** | 231,245 | 880 ms | 7,229 ms | 13,875 (\~6%) |


## Development Process with AI: Chat Gpt

- **Best Practices and Debugging**: ChatGPT assisted in creating boilerplate code for the microservice, data preprocessing pipelines, and feature engineering scripts, while providing guidance to resolve bugs efficiently.
  
- **Documentation and Clarity**: ChatGPT provided clear explanations and examples for writing comprehensive documentation, including the README file and architectural diagrams, ensuring a well-documented project structure.


## DEMO Video

Here is the link to our demo video: TO ADD
