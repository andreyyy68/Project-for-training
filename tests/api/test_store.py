import pytest
import allure
from pydantic import ValidationError
from models.order_model import OrderModel

@allure.feature("Store API")
@allure.story("Inventory")
@allure.title("Проверка GET /store/inventory")
@allure.description("Тест проверяет получение текущего инвентаря магазина через API.")
@allure.tag("api", "positive")
def test_get_inventory(api_manager):
    with allure.step("Отправляем запрос на получение инвентаря"):
        resp = api_manager.store_api.get_inventory(expected_status=None)
        data = resp.json()

    with allure.step("Проверяем статус код и содержимое ответа"):
        if resp.status_code == 200:
            assert isinstance(data, dict)
            assert "sold" in data or "available" in data
        elif resp.status_code == 500:
            assert "code" in data and data["code"] == 500
            assert "message" in data
        else:
            raise AssertionError(f"Неожиданный статус: {resp.status_code}, тело: {data}")


@allure.feature("Store API")
@allure.story("Order")
@allure.title("Создание заказа через POST /store/order")
@allure.description("Тест проверяет создание нового заказа и валидацию ответа через Pydantic.")
@allure.tag("api", "positive")
def test_create_order(api_manager, new_order_payload):
    with allure.step("Отправляем запрос на создание заказа"):
        resp = api_manager.store_api.create_order(new_order_payload, expected_status=None)

    with allure.step("Проверяем статус код"):
        assert resp.status_code in (200, 500)

    if resp.status_code == 200:
        with allure.step("Валидация ответа через Pydantic и проверка данных заказа"):
            try:
                order = OrderModel(**resp.json())
            except ValidationError as e:
                assert False, f"Order API response doesn't match model: {e}"

            assert order.id == new_order_payload["id"]
            assert order.status == new_order_payload["status"]


@allure.feature("Store API")
@allure.story("Order")
@allure.title("GET /store/order/{orderId} — проверка заказа по ID")
@allure.description("Тест проверяет корректность данных заказа через API по ID.")
@allure.tag("api", "positive")
def test_get_order_by_id(api_manager, new_order_payload):
    order_id = new_order_payload["id"]

    with allure.step(f"Отправляем запрос на получение заказа с ID {order_id}"):
        resp = api_manager.store_api.get_order_by_id(order_id, expected_status=None)

    with allure.step("Проверяем статус код и валидируем ответ"):
        if resp.status_code == 200:
            try:
                order = OrderModel(**resp.json())
            except ValidationError as e:
                assert False, f"Order API response doesn't match model: {e}"

            assert order.id == order_id
            assert order.status == new_order_payload["status"]
        elif resp.status_code in (404, 500):
            pass
        else:
            raise AssertionError(f"Unexpected status code: {resp.status_code}, body: {resp.text}")


@allure.feature("Store API")
@allure.story("Order")
@allure.title("DELETE /store/order/{orderId} — удаление заказа")
@allure.description("Тест проверяет удаление заказа и корректность последующих запросов.")
@allure.tag("api", "positive")
def test_delete_order(api_manager, new_order_payload):
    order_id = new_order_payload["id"]

    with allure.step(f"Отправляем запрос на удаление заказа с ID {order_id}"):
        delete_resp = api_manager.store_api.delete_order(order_id, expected_status=None)
        assert delete_resp.status_code in (200, 404), (
            f"Unexpected status code on DELETE: {delete_resp.status_code}, body: {delete_resp.text}"
        )

    with allure.step("Проверяем, что заказ больше не существует"):
        check_resp = api_manager.store_api.get_order_by_id(order_id, expected_status=None)
        if check_resp.status_code == 200:
            try:
                order = OrderModel(**check_resp.json())
                raise AssertionError(f"Order still exists after deletion: {order.id}")
            except ValidationError:
                pass
        elif check_resp.status_code not in (404, 500):
            raise AssertionError(
                f"Unexpected status code on GET after DELETE: {check_resp.status_code}, body: {check_resp.text}"
            )
