import json
from typing import List, Dict

from .abstract_storage import AbstractStorage


class JSONSaver(AbstractStorage):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализация хранилища"""
        self.__filename = filename

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавление вакансии в JSON-файл"""
        vacancies = self._load_vacancies()
        if not any(v["url"] == vacancy["url"] for v in vacancies):  # Проверка на дубли
            vacancies.append(vacancy)
            self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict) -> List[Dict]:
        """Получение вакансий по критериям"""
        vacancies = self._load_vacancies()
        filtered = []
        for vacancy in vacancies:
            matches = True
            for key, value in criteria.items():
                if key in vacancy and value.lower() not in vacancy[key].lower():
                    matches = False
                    break
            if matches:
                filtered.append(vacancy)
        return filtered

    def delete_vacancy(self, vacancy: Dict) -> None:
        """Удаление вакансии из JSON-файла"""
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v["url"] != vacancy["url"]]
        self._save_vacancies(vacancies)

    def _load_vacancies(self) -> List[Dict]:
        """Загрузка данных из JSON-файла"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: List[Dict]) -> None:
        """Сохранение данных в JSON-файл"""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)
