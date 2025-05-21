from typing import List
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам в описании"""
    if not filter_words:
        return vacancies
    return [
        vacancy for vacancy in vacancies
        if any(word.lower() in vacancy.description.lower() for word in filter_words)
    ]


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Фильтрация вакансий по диапазону зарплат"""
    if not salary_range:
        return vacancies
    try:
        low, high = map(int, salary_range.split("-"))
        return [
            vacancy for vacancy in vacancies
            if low <= vacancy.parsed_salary <= high
        ]
    except ValueError:
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате по убыванию"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ-N вакансий"""
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод вакансий в консоль"""
    if not vacancies:
        print("Вакансии не найдены.")
        return
    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия {i}:")
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print("-" * 50)
