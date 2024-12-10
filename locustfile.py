from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
    @task(1)
    def log_data(self):
        payload = {"transaction": "test_data"}
        self.client.post("/log", json=payload)

    @task(2)
    def predict(self):
        payload = {"transaction": "test_data"}
        self.client.post("/predict", json=payload)

class LoadTest(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000
    max_wait = 2000