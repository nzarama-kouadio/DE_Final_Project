# DE_Final_Project

[![apprunner](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/apprunner.yml) [![CICD](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml/badge.svg)](https://github.com/nzarama-kouadio/DE_Final_Project/actions/workflows/CICD.yml)



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
