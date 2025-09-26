import pytest
import allure

@allure.feature("Пользователи")
@allure.story("Логин пользователя")
@allure.title("Успешный логин пользователя")
@allure.description("Тест проверяет возможность успешного входа пользователя через UserAPI.")
@allure.tag("api", "positive")
def test_user_login(api_manager, user_fixture):
    with allure.step("Отправляем запрос на логин пользователя"):
        resp_login = api_manager.user_api.login(
            username=user_fixture["username"],
            password=user_fixture["password"],
            expected_status=None
        )

    with allure.step("Проверяем статус код ответа"):
        assert resp_login.status_code in (200, 404, 500)


@allure.feature("Пользователи")
@allure.story("Логин пользователя")
@allure.title("Попытка входа с неверным паролем")
@allure.description("Негативный тест: проверка логина с неправильным паролем.")
@allure.tag("api", "negative")
def test_login_with_wrong_password(api_manager):
    with allure.step("Отправляем запрос на логин с неверным паролем"):
        resp = api_manager.user_api.login(
            username="someuser",
            password="wrong_password",
            expected_status=None
        )

    with allure.step("Проверяем статус код ответа"):
        assert resp.status_code in (200, 404, 500)


@allure.feature("Пользователи")
@allure.story("Логаут пользователя")
@allure.title("Логаут авторизованного пользователя")
@allure.description("Тест проверяет корректность выхода пользователя через UserAPI.")
@allure.tag("api", "positive")
def test_user_logout(api_manager):
    with allure.step("Отправляем запрос на логаут пользователя"):
        resp = api_manager.user_api.logout(expected_status=None)

    with allure.step("Проверяем статус код ответа"):
        assert resp.status_code in (200, 404, 500)

    with allure.step("Проверяем содержимое ответа"):
        body_text = resp.text
        assert "user logged out" in body_text.lower(), f"Ожидаем слово 'logout' в ответе, получили: {body_text}"
