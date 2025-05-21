import unittest
from src.models.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def test_vacancy_init_valid(self):
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123", "100000 руб.", "Требуется опыт")
        self.assertEqual(vacancy.title, "Python Developer")
        self.assertEqual(vacancy.url, "https://hh.ru/vacancy/123")
        self.assertEqual(vacancy.salary, "100000 руб.")
        self.assertEqual(vacancy.description, "Требуется опыт")

    def test_vacancy_invalid_title(self):
        with self.assertRaises(ValueError):
            Vacancy("", "https://hh.ru/vacancy/123", "100000 руб.", "Требуется опыт")

    def test_vacancy_salary_not_specified(self):
        vacancy = Vacancy("Python Developer", "https://hh.ru/vacancy/123", None, "Требуется опыт")
        self.assertEqual(vacancy.salary, "Зарплата не указана")

    def test_vacancy_comparison(self):
        v1 = Vacancy("Dev1", "https://hh.ru/v1", "100000 руб.", "Описание")
        v2 = Vacancy("Dev2", "https://hh.ru/v2", "200000 руб.", "Описание")
        self.assertTrue(v2 > v1)
        self.assertFalse(v1 > v2)
        self.assertFalse(v1 == v2)


if __name__ == "__main__":
    unittest.main()
