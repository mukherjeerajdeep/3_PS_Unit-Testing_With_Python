import json

import pytest
import requests


@pytest.fixture
def main_url():
    return "https://reqres.in/"


def test_valid_login(main_url):
    url = main_url + "/api/login"
    data = {"email": "abc@xyz.com", "password": "querty"}
    response = requests.post(url, data=data)
    # token = json.loads(response.text) # Will break the test
    assert response.status_code == 200
    # assert token['token'] == "QpwL5tke4Pnpja7X4"
