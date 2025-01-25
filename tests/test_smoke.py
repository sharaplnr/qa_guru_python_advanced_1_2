import requests
from models.User import User

def test_health_check(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert response.status_code == 200

def test_status(app_url):
    response = requests.get(f"{app_url}/api/users")
    json_data = response.json()

    users = json_data.get("items", [])
    for user in users:
        User.model_validate(user)


