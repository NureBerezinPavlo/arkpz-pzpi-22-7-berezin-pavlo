import requests

class ServerClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_sensor_data(self, data):
        """Відправляє дані сенсорів на сервер через HTTP"""
        try:
            response = requests.post(f"{self.base_url}/sensors/", json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}