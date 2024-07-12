import requests
import logging


class HomemakerAPIClient(object):
    logger = logging.getLogger(__name__)

    def __init__(self, admin_token, base_url):
        self.admin_token = admin_token
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.admin_token}"}

    def get_homes(self):
        logging.debug("Attempting to get homes")
        url = f"{self.base_url}/homes"
        try:
            res = requests.get(url, headers=self.headers)
            res.raise_for_status()
            homes = res.json()
            logging.info(f"Successfully got {len(homes)} homes")
            return homes
        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to get homes: {e.response.status_code}")

    def delete_home(self, login):
        logging.debug(f"Attempting to delete {login}'s home")
        url = f"{self.base_url}/{login}"
        try:
            res = requests.delete(url, headers=self.headers)
            res.raise_for_status()
            logging.info(f"Successfully deleted {login}'s home")
            return True
        except requests.exceptions.HTTPError as e:
            logging.error(f"Failed to delete {login}'s home: {e.response.status_code}")
            return False
