import allure
import pytest
from data.user import gen_user_data
from methods.user_methods import UserMethods
from models.user import CreatedUser


@allure.parent_suite('Тестирование API сервиса Stellar Burgers')
@allure.suite('Обновление информации о пользователе')
class TestUpdateUser:
    @allure.sub_suite('Тестирование успешной смены информации о пользователе с '
                      'предварительной авторизацией')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа')
    @allure.description('Выполняем PATCH запрос /api/auth/user с указанием необходимых data '
                        'параметров для обновления (email, пароль или имя) и токена')
    @pytest.mark.parametrize('update_field', ['email', 'password', 'name'])
    def test_update_user_data_with_auth_status_code_is_ok(self,
                                                          create_user: CreatedUser,
                                                          update_field: str) -> None:
        status_code, response_data = UserMethods.update(
            update_data={update_field: gen_user_data()[update_field]},
            access_token=create_user.access_token)
        assert status_code == 200 and response_data['success'] is True

    @allure.sub_suite('Тестирование возврата ошибки при смене информации о пользователе без '
                      'предварительной авторизации')
    @allure.title('Проверка того, что система вернёт ошибку, если запрос призводится без '
                  'авторизации')
    @allure.description('Выполняем PATCH запрос /api/auth/user с указанием необходимых data '
                        'параметров для обновления (email, пароль или имя) НО без токена')
    @pytest.mark.parametrize('update_field', ['email', 'password', 'name'])
    def test_update_user_data_without_auth_status_code_is_unauthorized(self,
                                                                       create_user: CreatedUser,
                                                                       update_field: str) -> None:
        status_code, response_data = UserMethods.update(
            update_data={update_field: gen_user_data()[update_field]})
        assert (status_code == 401 and
                response_data['success'] is False and
                response_data['message'] == 'You should be authorised')
