import unittest
import os
from src.storage.json_storage import JSONSaver


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver(self.filename)
        self.vacancy = {
            "title": "Test Vacancy",
            "url": "https://hh.ru/test",
            "salary": "100000 руб.",
            "description": "Test description"
        }

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies({})
        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]["title"], "Test Vacancy")

    def test_delete_vacancy(self):
        self.saver.add_vacancy(self.vacancy)
        self.saver.delete_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies({})
        self.assertEqual(len(vacancies), 0)

    def test_get_vacancies_with_criteria(self):
        self.saver.add_vacancy(self.vacancy)
        vacancies = self.saver.get_vacancies({"title": "Test"})
        self.assertEqual(len(vacancies), 1)
        vacancies = self.saver.get_vacancies({"title": "Nonexistent"})
        self.assertEqual(len(vacancies), 0)


if __name__ == "__main__":
    unittest.main()
