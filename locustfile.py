from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task(1)
    def log_data(self):
        self.client.get("/health")

    @task(2)
    def predict(self):
        payload = [
            {
                "TransactionID": "1",
                "Timestamp": "2024-12-10T12:00:00",
                "MerchantID": "101",
                "Amount": 100.5,
                "CustomerID": "202",
                "TransactionAmount": 150.75,
                "AnomalyScore": 0.5,
                "Category": "Online",
                "CustomerAge": 35,
                "AccountBalance": 5000.25,
                "SuspiciousFlag": 0,
                "LastLogin": "2024-12-09T15:00:00"
            }
            ]
        self.client.post("/predict", json=payload)


class LoadTest(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000
