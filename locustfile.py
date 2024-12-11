from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task(1)
    def log_data(self):
        self.client.get("/health")

    @task(2)
    def predict(self):
        payload = {
            "transaction_id": "1",
            "amount": 100,
            "timestamp": "2024-12-09T12:00:00",
            "merchant": "Amazon",
        }
        self.client.post("/predict",payload)


class LoadTest(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000
