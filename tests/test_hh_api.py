import unittest
from unittest.mock import patch
from src.api.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    @patch("requests.get")
    def test_get_vacancies_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"items": [{"name": "Test", "alternate_url": "http://test"}]}
        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["name"], "Test")

    @patch("requests.get")
    def test_connect_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        api = HeadHunterAPI()
        with self.assertRaises(ConnectionError):
            api._connect()


if __name__ == "__main__":
    unittest.main()
