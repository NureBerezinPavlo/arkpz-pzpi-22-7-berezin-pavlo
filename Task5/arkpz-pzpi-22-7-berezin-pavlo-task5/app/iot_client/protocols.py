import requests

class ServerClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None

    def authenticate(self, email, password):
        """Отримує токен за допомогою email і пароля"""
        try:
            response = requests.post(
                f"{self.base_url}/admins/login",
                json={"email": email, "password": password}
            )
            response.raise_for_status()
            self.token = response.json().get("access_token")
            return {"success": True, "message": "Authenticated successfully"}
        except requests.RequestException as e:
            return {"success": False, "message": str(e)}

    def send_sensor_data(self, data):
        """Відправляє дані сенсорів на сервер через HTTP"""
        if not self.token:
            return {"error": "No token provided. Authenticate first."}
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.post(
                f"{self.base_url}/sensors/", json=data, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}