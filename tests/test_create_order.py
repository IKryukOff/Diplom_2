import allure
from data.ingredients import get_random_ingredients
from methods.order_methods import OrderMethods
from models.user import CreatedUser


@allure.parent_suite('Тестирование API сервиса Stellar Burgers')
@allure.suite('Создание заказа')
class TestCreateOrder:
    @allure.sub_suite('Тестирование успешного создания заказа с указанием ингредиентов и '
                      'с предварительной авторизацией')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа '
                  'и владельцем заказа является авторизовавшийся пользователь')
    @allure.description('Выполняем POST запрос /api/orders с указанием необходимых ingredients в '
                        'data и токена')
    def test_create_order_with_ingredients_and_auth_status_code_is_ok(
            self, create_user: CreatedUser) -> None:
        status_code, response_data = OrderMethods.create_order(
            ingredients=get_random_ingredients(), access_token=create_user.access_token)
        assert (status_code == 200 and
                isinstance(response_data, dict) and
                response_data['success'] is True and
                response_data['order'].get('owner') is not None and
                response_data['order']['owner']['name'] == create_user.register_data['name'])

    @allure.sub_suite('Тестирование успешного создания заказа с указанием ингредиентов и '
                      'без предварительной авторизации')
    @allure.title('Проверка того, что успешный запрос возвращает "success": true в теле ответа '
                  'и у заказа отсутствует владелец')
    @allure.description('Выполняем POST запрос /api/orders с указанием необходимых ingredients в '
                        'data и без токена')
    def test_create_order_with_ingredients_and_without_auth_status_code_is_ok(self) -> None:
        status_code, response_data = OrderMethods.create_order(ingredients=get_random_ingredients())
        assert (status_code == 200 and
                isinstance(response_data, dict) and
                response_data['success'] is True and
                response_data['order'].get('owner') is None)

    @allure.sub_suite('Тестирование ошибки при создания заказа без указания игредиентов')
    @allure.title('Проверка того, что запрос возвращает ошибку с сообщением о необходимости '
                  'ингредиентов')
    @allure.description('Выполняем POST запрос /api/orders без указания ingredients в data')
    def test_create_order_without_ingredients_satus_code_is_bad_request(self) -> None:
        status_code, response_data = OrderMethods.create_order()
        assert (status_code == 400 and
                isinstance(response_data, dict) and
                response_data['success'] is False and
                response_data['message'] == 'Ingredient ids must be provided')

    @allure.sub_suite('Тестирование ошибки при создания заказа с указанием несуществующего '
                      'игредиента')
    @allure.title('Проверка того, что запрос возвращает ошибку с сообщением о некорректном '
                  'указании ингредиента')
    @allure.description('Выполняем POST запрос /api/orders с измененным хэшем ingredients в data')
    def test_create_order_with_unknown_ingredients_satus_code_is_bad_request(self) -> None:
        unknown_ingredient = get_random_ingredients(1)[0][::-1]
        status_code, response_data = OrderMethods.create_order(ingredients=[unknown_ingredient])
        assert (status_code == 400 and
                isinstance(response_data, dict) and
                response_data['success'] is False and
                response_data['message'] == 'One or more ids provided are incorrect')

    @allure.sub_suite('Тестирование ошибки при создания заказа с указанием некорректного значения '
                      'хэша ингредиента')
    @allure.title('Проверка того, что запрос возвращает ошибку с кодом 500')
    @allure.description('Выполняем POST запрос /api/orders с неправильным хэшем ingredietns в data '
                        '(неправильный размер)')
    def test_create_order_with_invalid_ingredients_satus_code_is_error(self) -> None:
        invalid_ingredient = get_random_ingredients(1)[0] + '1'
        status_code, _ = OrderMethods.create_order(ingredients=[invalid_ingredient])
        assert status_code == 500
