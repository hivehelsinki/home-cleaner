import pytest
from unittest.mock import patch, mock_open
import yaml
import logging

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


@pytest.fixture
def homes():
    return ["user1", "user2", "user3", "user4", "user5"]


@pytest.fixture
def students():
    return ["user1", "user2", "user3"]


@pytest.fixture
def inactive_students():
    return ["user1", "user2"]


@pytest.fixture
def mock_config(config_data):
    with patch("builtins.open", mock_open(read_data=config_data)), patch(
        "app.helpers.load_config.load_config", return_value=yaml.safe_load(config_data)
    ), patch.dict("app.main.config", yaml.safe_load(config_data)):
        yield


def test_get_homes(requests_mock, base_url, mock_config):
    """
    Test the get_homes function for successful API response and correct filtering of homes.
    """
    home_service_response = {
        "status_code": 200,
        "json": [
            {
                "busy": False,
                "enabled": True,
                "identifier": "user1",
                "index": 1,
                "size": 5003804672,
            },
            {
                "busy": False,
                "enabled": True,
                "identifier": "user2",
                "index": 2,
                "size": 5003804672,
            },
        ],
    }

    from app.main import get_homes

    requests_mock.get(f"{base_url}/homes", **home_service_response)

    homes = get_homes()

    logger.debug("Homes: %s", homes)
    assert homes == ["user2"]


def test_get_homes_no_homes_exit(requests_mock, base_url, mock_config):
    """
    Test the get_homes function when no homes are returned by the API, ensuring it exits as expected.
    """
    home_service_response = {"status_code": 200, "json": []}

    from app.main import get_homes

    requests_mock.get(f"{base_url}/homes", **home_service_response)

    with pytest.raises(SystemExit):
        get_homes()


def test_get_homes_with_exception(requests_mock, base_url, mock_config):
    """
    Test the get_homes function for handling server errors and raising SystemExit.
    """
    home_service_response = {"status_code": 500, "json": []}

    from app.main import get_homes

    requests_mock.get(f"{base_url}/homes", **home_service_response)

    with pytest.raises(SystemExit):
        get_homes()


def test_check_students_profile_creation_dates(homes, mock_config):
    """
    Test the check_students_profile_creation_dates function to filter old homes based on student profile creation dates.
    """
    from app.main import check_students_profile_creation_dates

    with patch("app.main.make_range") as mock_make_range, patch(
        "app.main.make_homes_chunks"
    ) as mock_make_homes_chunks, patch(
        "app.main.ic.pages_threaded"
    ) as mock_pages_threaded:
        mock_make_range.return_value = "mocked_date_range"
        mock_make_homes_chunks.return_value = [
            ["user1", "user2"],
            ["user3", "user4", "user5"],
        ]
        mock_pages_threaded.side_effect = [
            [{"login": "user1"}, {"login": "user3"}],  # Response for first chunk
            [{"login": "user4"}],  # Response for second chunk
        ]

        old_homes = check_students_profile_creation_dates(homes)

        logger.debug("Old homes: %s", old_homes)
        assert old_homes == ["user2", "user5"]


def test_get_inactive_students(students, mock_config):
    """
    Test the get_inactive_students function to identify inactive students based on API responses.
    """
    from app.main import get_inactive_students

    with patch("app.main.make_date_payload") as mock_make_date_payload, patch(
        "app.main.ic.pages_threaded"
    ) as mock_pages_threaded:
        mock_make_date_payload.return_value = "mocked_payload"
        mock_pages_threaded.side_effect = [{}, {"some_data": "value"}, {}]

        inactive_students = get_inactive_students(students)

        logger.debug("Inactive students: %s", inactive_students)
        assert inactive_students == ["user1", "user3"]

        mock_pages_threaded.side_effect = [{"some_data": "value"}] * len(students)
        with pytest.raises(SystemExit):
            get_inactive_students(students)


def test_get_inactive_students_with_exception(students, mock_config):
    """
    Test the get_inactive_students function to handle exceptions from the API properly.
    """
    from app.main import get_inactive_students

    with patch("app.main.make_date_payload") as mock_make_date_payload, patch(
        "app.main.ic.pages_threaded"
    ) as mock_pages_threaded:
        mock_make_date_payload.return_value = "mocked_payload"
        mock_pages_threaded.side_effect = [{}, Exception("Mocked exception"), {}]

        inactive_students = get_inactive_students(students)

        logger.debug("Inactive students: %s", inactive_students)
        assert inactive_students == ["user1", "user3"]


def test_get_inactive_students_with_no_students_found(students):
    """
    Test the get_inactive_students function to handle exceptions from the API properly.
    """
    from app.main import get_inactive_students

    with patch("app.main.make_date_payload") as mock_make_date_payload, patch(
        "app.main.ic.pages_threaded"
    ) as mock_pages_threaded:
        mock_make_date_payload.return_value = "mocked_payload"
        mock_pages_threaded.return_value = {"something": "value"}

        with pytest.raises(SystemExit):
            get_inactive_students(students)


# New test cases for delete_homes
def test_delete_homes_success(inactive_students):
    from app.main import delete_homes
    from app.main import hmk

    with patch.object(hmk, "delete_home", return_value=True) as mock_delete_home:
        delete_homes(inactive_students)

        # Ensure delete_home is called for each inactive student
        assert mock_delete_home.call_count == len(inactive_students)
        for student in inactive_students:
            mock_delete_home.assert_any_call(student)


def test_delete_homes_partial_failure(inactive_students):
    from app.main import delete_homes
    from app.main import hmk

    with patch.object(
        hmk, "delete_home", side_effect=[True, False]
    ) as mock_delete_home:
        delete_homes(inactive_students)

        # Ensure delete_home is called for each inactive student
        assert mock_delete_home.call_count == len(inactive_students)
        for student in inactive_students:
            mock_delete_home.assert_any_call(student)


def test_delete_homes_all_failure(inactive_students):
    from app.main import delete_homes
    from app.main import hmk

    with patch.object(hmk, "delete_home", return_value=False) as mock_delete_home:
        delete_homes(inactive_students)

        # Ensure delete_home is called for each inactive student
        assert mock_delete_home.call_count == len(inactive_students)
        for student in inactive_students:
            mock_delete_home.assert_any_call(student)


def test_check_that_homes_are_deleted(inactive_students):
    from app.main import check_that_homes_are_deleted

    with patch("app.main.get_homes", return_value=["user3", "user4", "user5"]), patch(
        "logging.info"
    ) as mock_logging_info:
        check_that_homes_are_deleted(inactive_students)
        mock_logging_info.assert_any_call("All homes are deleted.")


def test_check_that_homes_are_deleted_not_deleted(inactive_students):
    from app.main import check_that_homes_are_deleted

    with patch(
        "app.main.get_homes", return_value=["user1", "user2", "user3", "user4", "user5"]
    ), patch("logging.error") as mock_logging_error:
        check_that_homes_are_deleted(inactive_students)
        mock_logging_error.assert_any_call("\033[0;31mFailed to delete 2 homes:")
        mock_logging_error.assert_any_call("user1, user2")
