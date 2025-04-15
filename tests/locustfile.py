from locust import HttpUser, task, between


class ApiTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_consumidores(self):
        self.client.get("/api/consumidores/")

    @task
    def create_consumidor(self):
        self.client.post("/api/consumidores/", json={"nome": "Teste Locust"})
