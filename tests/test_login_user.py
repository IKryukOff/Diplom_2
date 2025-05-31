import allure
import pytest
from methods.user_methods import UserMethods
from models.user import CreatedUser


@allure.parent_suite('Тестирование API сервиса Stellar Burgers')
@allure.suite('Авторизация пользователя')
class TestLoginUser:
    @allure.sub_suite('Тестирование успешной авторизации пользователя')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа')
    @allure.description('Выполняем POST запрос /api/auth/login с указанием необходимых data '
                        'параметров (email, пароль)')
    def test_login_user_status_code_is_ok(self, create_user: CreatedUser) -> None:
        status_code, response_data = UserMethods.login(user_data=create_user.login_data)
        assert (status_code == 200 and
                isinstance(response_data, dict) and
                response_data['success'] is True)

    @allure.sub_suite('Тестирование возврата ошибки при некорректной авторизации пользователя')
    @allure.title('Проверка того, что система вернёт ошибку, если неправильно указать email или '
                  'пароль пользователя')
    @allure.description('Выполняем POST запрос /api/auth/login с указанием невенрного значения '
                        'data параметров (email, пароль)')
    @pytest.mark.parametrize('incorrect_field', ['email', 'password'])
    def test_login_user_with_incorrect_data_status_code_is_unauthorized(
            self, create_user: CreatedUser, incorrect_field: str) -> None:
        status_code, response_data = UserMethods.login(user_data={**create_user.login_data,
                                                                  incorrect_field: 'incorrect'})
        assert (status_code == 401 and
                isinstance(response_data, dict) and
                response_data['success'] is False and
                response_data['message'] == 'email or password are incorrect')
