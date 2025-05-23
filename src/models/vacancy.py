from typing import Optional, Dict, List


def _validate_title(title: str) -> str:
    """Валидация названия вакансии"""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Название вакансии должно быть непустой строкой")
    return title.strip()


def _validate_url(url: str) -> str:
    """Валидация URL вакансии"""
    if not isinstance(url, str) or not url.startswith("http"):
        raise ValueError("URL должен быть валидной строкой, начинающейся с http")
    return url


def _validate_description(description: Optional[str]) -> str:
    """Валидация описания"""
    return description if description and isinstance(description, str) else "Описание не указано"


def _validate_salary(salary: Optional[str]) -> str:
    """Валидация зарплаты"""
    return salary if salary and isinstance(salary, str) else "Зарплата не указана"


class Vacancy:
    """Класс для представления вакансии"""

    __slots__ = ("_title", "_url", "_salary", "_description")

    def __init__(self, title: str, url: str, salary: Optional[str], description: Optional[str]) -> None:
        """Инициализация вакансии"""
        self._title = _validate_title(title)
        self._url = _validate_url(url)
        self._salary = _validate_salary(salary)
        self._description = _validate_description(description)

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary(self) -> str:
        return self._salary

    @property
    def description(self) -> str:
        return self._description

    @property
    def parsed_salary(self) -> float:
        """Возвращает числовое значение зарплаты для сравнения."""
        return self._parse_salary()

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий по зарплате"""
        return self._parse_salary() < other._parse_salary()

    def __gt__(self, other: "Vacancy") -> bool:
        return self._parse_salary() > other._parse_salary()

    def __eq__(self, other: "Vacancy") -> bool:
        return self._parse_salary() == other._parse_salary()

    def _parse_salary(self) -> float:
        """Парсинг зарплаты для сравнения"""
        if self._salary == "Зарплата не указана":
            return 0
        try:
            # Предполагаем, что зарплата в формате "100000-150000 руб." или "100000 руб."
            salary_str = self._salary.split()[0]
            if "-" in salary_str:
                low, high = map(int, salary_str.split("-"))
                return (low + high) / 2
            return float(salary_str)
        except (ValueError, IndexError):
            return 0

    def to_dict(self) -> Dict:
        """Преобразование вакансии в словарь"""
        return {
            "title": self._title,
            "url": self._url,
            "salary": self._salary,
            "description": self._description
        }

    @classmethod
    def cast_to_object_list(cls, vacancies: List[Dict]) -> List["Vacancy"]:
        """Преобразование списка словарей в список объектов Vacancy"""
        result = []
        for vacancy in vacancies:
            title = vacancy.get("name", "")
            url = vacancy.get("alternate_url", "")
            if vacancy.get("salary"):
                salary = vacancy.get("salary", {}).get("from") or vacancy.get("salary", {}).get("to") or None
            else:
                salary = None
            salary_str = f"{salary} руб." if salary else None
            description = vacancy.get("snippet", {}).get("requirement", "Описание не указано")
            try:
                result.append(cls(title, url, salary_str, description))
            except ValueError:
                continue
        return result