import allure
import pytest
from methods.user_methods import UserMethods


@allure.parent_suite('Тестирование API сервиса Stellar Burgers')
@allure.suite('Создание пользователя')
class TestCreateUser:
    @allure.sub_suite('Тестирование успешного создания пользователя')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа')
    @allure.description('Выполняем POST запрос /api/auth/register с указанием необходимых data '
                        'параметров (email, пароль, имя)')
    def test_create_user_status_code_is_ok(self, user_data: dict[str, str]) -> None:
        status_code, response_data = UserMethods.register(user_data=user_data)
        assert status_code == 200 and response_data['success'] is True

    @allure.sub_suite('Тестирование возврата ошибки при создании уже существующего пользователя')
    @allure.title('Проверка того, что запрос возвращает сообщение "User already exists"')
    @allure.description('Выполняем POST запрос /api/auth/register с указанием data параметров '
                        '(email, пароль, имя) уже зарегестрированного ранее пользователя')
    def test_create_already_exists_user_status_code_is_forbidden(
            self, create_user: tuple[dict[str, str], str]) -> None:
        status_code, response_data = UserMethods.register(user_data=create_user[0])
        assert (status_code == 403 and
                response_data['success'] is False and
                response_data['message'] == 'User already exists')

    @allure.sub_suite('Тестирование возврата ошибки при создании пользователя c неполными данными')
    @allure.title('Проверка того, что запрос возвращает сообщение о необходимости указать все поля')
    @allure.description('Выполняем POST запрос /api/auth/register без указания email, пароля или '
                        'имени и ожидаем ошибку отсутствия необходимых данных')
    @pytest.mark.parametrize('excluded_data_field', ['email', 'password', 'name'])
    def test_create_user_with_incorrect_data_status_code_is_forbidden(
            self, user_data: dict[str, str], excluded_data_field: str) -> None:
        user_data.pop(excluded_data_field)
        status_code, response_data = UserMethods.register(user_data=user_data)
        assert (status_code == 403 and
                response_data['success'] is False and
                response_data['message'] == 'Email, password and name are required fields')
