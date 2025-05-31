import allure
from data.ingredients import get_random_ingredients
from methods.order_methods import OrderMethods
from models.user import CreatedUser


@allure.parent_suite('Тестирование API сервиса Stellar Burgers')
@allure.suite('Получение заказов пользователя')
class TestGetOrders:
    @allure.sub_suite('Тестирование успешного получения информации о заказах пользователя с '
                      'предварительной авторизацией и созданием заказа')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа '
                  'и номер предварительно созданного заказа имеется в теле ответа')
    @allure.description('Выполняем GET запрос /api/orders c указанием токена, предварительно '
                        'создаем заказ от этого же пользователя')
    def test_get_orders_with_auth_status_code_is_ok(self,
                                                    create_user: CreatedUser) -> None:
        _, create_response_data = OrderMethods.create_order(ingredients=get_random_ingredients(),
                                                            access_token=create_user.access_token)
        status_code, response_data = OrderMethods.get_orders(access_token=create_user.access_token)
        assert (status_code == 200 and
                (isinstance(response_data, dict) and isinstance(create_response_data, dict)) and
                response_data['success'] is True and
                create_response_data['order']['number'] == response_data['orders'][0]['number'])

    @allure.sub_suite('Тестирование ошибки получения информации о заказов пользователя без '
                      'предварительной авторизации')
    @allure.title('Проверка того, что запрос возвращает ошибку неавторизованного пользователя')
    @allure.description('Выполняем GET запрос /api/orders без указания токена')
    def test_get_orders_without_auth_status_code_is_unauthorized(self) -> None:
        status_code, response_data = OrderMethods.get_orders()
        assert (status_code == 401 and
                isinstance(response_data, dict) and
                response_data['success'] is False and
                response_data['message'] == 'You should be authorised')
