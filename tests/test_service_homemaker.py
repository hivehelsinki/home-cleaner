import pytest
from app.main import get_homes
from app.services.homemaker import HomemakerAPIClient

@pytest.fixture
def base_url():
    return "http://storage-linux.hive.fi/api/v1"

def test_service_get_homes(requests_mock, base_url):
    home_service_response = {
        "status_code": 200,
        "json": [
            {"busy": False,"enabled":True,"identifier":"clem","index":1,"size":5003804672},
            {"busy":False,"enabled":True,"identifier":"titus","index":2,"size":5003804672}
        ],
    }

    client = HomemakerAPIClient(admin_token="mock_token", base_url=base_url)
    
    requests_mock.get(f"{base_url}/homes", **home_service_response)

    homes = client.get_homes()

    assert homes == [
        {"busy": False,"enabled":True,"identifier":"clem","index":1,"size":5003804672},
        {"busy":False,"enabled":True,"identifier":"titus","index":2,"size":5003804672}
    ]


# @pytest.mark.xfail
def test_get_homes(requests_mock, base_url):
    home_service_response = {
        "status_code": 200,
        "json": [
            {"busy": False,"enabled":True,"identifier":"user1","index":1,"size":5003804672},
            {"busy":False,"enabled":True,"identifier":"user2","index":2,"size":5003804672}
        ],
    }

    requests_mock.get(f"{base_url}/homes", **home_service_response)

    homes = get_homes()

    assert homes == ['user1', 'user2']