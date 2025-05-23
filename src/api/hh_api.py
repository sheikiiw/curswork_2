from typing import Dict, List

import requests

from .abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API hh.ru"""

    def __init__(self) -> None:
        self.__base_url: str = "https://api.hh.ru"
        self.__vacancies_url: str = f"{self.__base_url}/vacancies"

    def _connect(self) -> None:
        """Подключение к API hh.ru и проверка доступности"""
        try:
            response = requests.get(self.__vacancies_url)
            if response.status_code != 200:
                raise ConnectionError(f"Ошибка подключения к API: {response.status_code}")
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {str(e)}")

    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получение вакансий с hh.ru по поисковому запросу"""
        self._connect()
        params = {
            "text": search_query,
            "per_page": 100,
            "area": 1,  # Код региона (1 - Москва)
            "only_with_salary": False
        }
        try:
            response = requests.get(self.__vacancies_url, params=params)
            if response.status_code != 200:
                raise ValueError(f"Ошибка получения данных: {response.status_code}")
            return response.json().get("items", [])
        except requests.RequestException as e:
            raise ValueError(f"Ошибка запроса к API: {str(e)}")
