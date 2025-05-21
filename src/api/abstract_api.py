from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def _connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict]:
        """Получение списка вакансий по поисковому запросу"""
        pass
