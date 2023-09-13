import random, json
from locust import HttpUser, task, between


class MyUser(HttpUser):

    @task
    def test_create_staff_user(self):
        payload = {
            'firstName': 'Staff',
            'lastName': 'User',
            'emailAddress': 'staff.user@example.com',
            'password': 'password'
        }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(
            '/api/v1/user/create', data=json.dumps(payload), headers=headers)
        assert response.status_code == 201


    @task(1)
    def login(self):
        response = self.client.post(
            "/api/v1/user/login",
            json={"emailAddress": 'staff.user@example.com',
                  "password": "password"}
        )
        if response.status_code == 200:
            self.token = response.json().get("payload", {}).get("token")
        else:
            self.token = None

    @task(2)
    def access_protected_endpoint(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.get(
                "/api/v1/your_protected_endpoint", headers=headers)
            if response.status_code != 200:
                self.environment.runner.quit() 
