import pytest
import requests_mock
import json
from app.main import get_homes


@pytest.fixture
def config():
    # Mocking the config object
    return {
        "homemaker": {"base-url": "http://example.com/api/v1", "admin-token": "token"}
    }


@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as m:
        yield m


def load_stub():
    with open("homemaker-mock/stub.json") as f:
        return json.load(f)


def test_get_homes_200(requests_mock_fixture, mocker, config):
    mocker.patch("app.main.config", config)

    stub_data = load_stub()
    for mapping in stub_data["mappings"]:
        url = (
            f"{config['homemaker']['base-url']}{mapping['request']['urlPathTemplate']}"
        )
        method = mapping["request"]["method"].lower()
        response = mapping["response"]

        requests_mock_fixture.register_uri(
            method,
            url,
            status_code=response["status"],
            json=response["jsonBody"],
            headers=response["headers"],
        )

    homes = get_homes()

    expected_identifiers = [home["identifier"] for home in response["jsonBody"]]
    assert homes == expected_identifiers


def test_get_homes_fail(requests_mock_fixture, mocker, config):
    fail_codes = [400, 401, 403, 404, 500]
    for fail_code in fail_codes:
        mocker.patch("app.main.config", config)

        stub_data = load_stub()
        for mapping in stub_data["mappings"]:
            url = f"{config['homemaker']['base-url']}{mapping['request']['urlPathTemplate']}"
            method = mapping["request"]["method"].lower()
            requests_mock_fixture.reset()
            requests_mock_fixture.register_uri(method, url, status_code=fail_code)
        with pytest.raises(SystemExit):
            get_homes()
