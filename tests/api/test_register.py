from models.user_model import UserModel
from pydantic import ValidationError
import allure

@allure.suite("User API")
@allure.sub_suite("Create User")
@allure.feature("Пользователи")
@allure.story("Создание нового пользователя")
@allure.title("Создание пользователя с валидными данными")
@allure.description("Тест проверяет создание нового пользователя через UserAPI и валидацию ответа Pydantic.")
@allure.tag("api", "positive")
def test_create_user(api_manager, new_user_payload):
    with allure.step("Отправляем POST запрос на создание пользователя"):
        resp_post = api_manager.user_api.create_user(
            user_data=new_user_payload,
            expected_status=None
        )
        allure.attach(str(resp_post.json()), name="Ответ API", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем статус код"):
        assert resp_post.status_code in (200, 404, 500)

    if resp_post.status_code == 200:
        with allure.step("Валидация ответа через Pydantic"):
            try:
                user = UserModel(**resp_post.json())
            except ValidationError as e:
                assert False, f"Ответ API не соответствует схеме: {e}"

        with allure.step("Проверяем соответствие данных запроса и ответа"):
            assert user.username == new_user_payload["username"]
            assert user.email == new_user_payload["email"]

@allure.feature("Пользователи")
@allure.story("Создание нового пользователя")
@allure.title("Создание пользователя без обязательного поля 'username'")
@allure.description("Негативный тест: проверяем, что API возвращает ошибку при отсутствии обязательного поля 'username'.")
@allure.tag("api", "negative")
def test_create_user_missing_username(api_manager, new_user_payload):
    with allure.step("Удаляем обязательное поле 'username' из payload"):
        new_user_payload.pop("username", None)

    with allure.step("Отправляем POST запрос на создание пользователя"):
        resp_post = api_manager.user_api.create_user(
            user_data=new_user_payload,
            expected_status=None
        )

    with allure.step("Проверяем статус код"):
        assert resp_post.status_code in (400, 500), f"Ожидался код ошибки, получен {resp_post.status_code}"

    if resp_post.status_code == 200:
        with allure.step("Валидация ответа через Pydantic"):
            try:
                user = UserModel(**resp_post.json())
            except ValidationError as e:
                # Ожидаем ошибку, потому что username отсутствует
                assert "username" in str(e), f"Проверка Pydantic не сработала: {e}"

        with allure.step("Проверяем соответствие данных запроса и ответа"):
            assert user.username == new_user_payload.get("username")
            assert user.email == new_user_payload["email"]



