import pytest
from unittest.mock import patch
import logging
from app.services.homemaker import HomemakerAPIClient

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.fixture
def base_url():
    return "http://localhost/api/v1"


@pytest.fixture
def config_data(base_url):
    return f"""
    god_mode_accounts:
      - user1
    homemaker:
      admin_token: mock_token
      base_url: {base_url}
    intra:
      client: mock_client
      secret: mock_secret
    campus_id: mock_campus
    """


def test_service_get_homes(requests_mock, base_url):
    with patch("logging.info") as mock_logging_info:
        home_service_response = {
            "status_code": 200,
            "json": [
                {
                    "busy": False,
                    "enabled": True,
                    "identifier": "clem",
                    "index": 1,
                    "size": 5003804672,
                },
                {
                    "busy": False,
                    "enabled": True,
                    "identifier": "titus",
                    "index": 2,
                    "size": 5003804672,
                },
            ],
        }

        client = HomemakerAPIClient(admin_token="mock_token", base_url=base_url)

        requests_mock.get(f"{base_url}/homes", **home_service_response)

        homes = client.get_homes()

        assert homes == [
            {
                "busy": False,
                "enabled": True,
                "identifier": "clem",
                "index": 1,
                "size": 5003804672,
            },
            {
                "busy": False,
                "enabled": True,
                "identifier": "titus",
                "index": 2,
                "size": 5003804672,
            },
        ]
        mock_logging_info.assert_called_with(
            f"Successfully got {len(home_service_response['json'])} homes"
        )
