from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONSaver
from src.utils.helpers import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, \
    print_vacancies


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем."""
    print("Добро пожаловать в парсер вакансий hh.ru!")

    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    search_query = input("Введите поисковый запрос (например, Python): ").strip()
    if not search_query:
        print("Ошибка: поисковый запрос не может быть пустым.")
        return

    top_n = input("Введите количество вакансий для вывода в топ N: ").strip()
    try:
        top_n = int(top_n)
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("Ошибка: введите положительное целое число.")
        return

    filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
    salary_range = input("Введите диапазон зарплат (например, 100000-150000): ").strip()

    # Получение вакансий
    try:
        hh_vacancies = hh_api.get_vacancies(search_query)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

        # Сохранение в JSON
        for vacancy in vacancies_list:
            json_saver.add_vacancy(vacancy.to_dict())

        # Фильтрация и сортировка
        filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        # Вывод результатов
        print_vacancies(top_vacancies)

        # Пример удаления вакансии
        if top_vacancies:
            json_saver.delete_vacancy(top_vacancies[0].to_dict())
            print("Первая вакансия удалена из файла.")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    user_interaction()
