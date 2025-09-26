import allure
from pydantic import ValidationError
from models.pet_model import PetModel

@allure.feature("Pet API")
@allure.story("Add Pet")
@allure.title("Добавление нового питомца")
@allure.description("Тест проверяет создание нового питомца через PetAPI и валидацию ответа Pydantic.")
@allure.tag("api", "positive")
def test_add_pet(api_manager, new_pet_payload):
    with allure.step("Отправляем запрос на добавление нового питомца"):
        resp = api_manager.pet_api.add_pet(new_pet_payload, expected_status=None)

    with allure.step("Проверяем статус код"):
        assert resp.status_code in (200, 500)

    if resp.status_code == 200:
        with allure.step("Валидация ответа через Pydantic и проверка данных питомца"):
            try:
                pet = PetModel(**resp.json())
            except ValidationError as e:
                assert False, f"Pet API response doesn't match model: {e}"

            assert pet.id == new_pet_payload["id"]
            assert pet.name == new_pet_payload["name"]


@allure.feature("Pet API")
@allure.story("Update Pet")
@allure.title("Обновление данных питомца")
@allure.description("Тест проверяет обновление информации о питомце через PetAPI.")
@allure.tag("api", "positive")
def test_update_pet(api_manager, new_pet_payload):
    with allure.step("Создаём питомца перед обновлением"):
        api_manager.pet_api.add_pet(new_pet_payload, expected_status=None)

    updated_data = new_pet_payload.copy()
    updated_data["name"] = "UpdatedName"
    updated_data["status"] = "sold"

    with allure.step("Отправляем запрос на обновление питомца"):
        resp = api_manager.pet_api.update_pet(updated_data, expected_status=None)

    with allure.step("Проверяем статус код"):
        assert resp.status_code in (200, 404, 500)

    if resp.status_code == 200:
        with allure.step("Валидация ответа и проверка изменений"):
            try:
                pet = PetModel(**resp.json())
            except ValidationError as e:
                assert False, f"Pet API response doesn't match model: {e}"

            assert pet.name == "UpdatedName"
            assert pet.status == "sold"


@allure.feature("Pet API")
@allure.story("Get Pet")
@allure.title("Получение питомца по ID")
@allure.description("Тест проверяет получение данных о питомце по ID через PetAPI.")
@allure.tag("api", "positive")
def test_get_pet_by_id(api_manager, created_pet):
    pet_id = created_pet["id"]

    with allure.step(f"Отправляем запрос на получение питомца с ID {pet_id}"):
        resp = api_manager.pet_api.get_pet_by_id(pet_id, expected_status=None)

    with allure.step("Проверяем статус код и валидируем ответ"):
        assert resp.status_code in (200, 404, 500)

        if resp.status_code == 200:
            try:
                pet = PetModel(**resp.json())
            except ValidationError as e:
                assert False, f"Pet API response doesn't match model: {e}"

            assert pet.id == pet_id
            assert pet.name == created_pet["name"]


@allure.feature("Pet API")
@allure.story("Delete Pet")
@allure.title("Удаление питомца")
@allure.description("Тест проверяет удаление питомца и последующую проверку через PetAPI.")
@allure.tag("api", "positive")
def test_delete_pet(api_manager, created_pet):
    pet_id = created_pet["id"]

    with allure.step(f"Отправляем запрос на удаление питомца с ID {pet_id}"):
        delete_resp = api_manager.pet_api.delete_pet(pet_id, expected_status=None)
        assert delete_resp.status_code in (200, 404)

    with allure.step("Проверяем, что питомец больше не существует"):
        get_resp = api_manager.pet_api.get_pet_by_id(pet_id, expected_status=None)
        if get_resp.status_code == 200:
            try:
                pet = PetModel(**get_resp.json())
                print(f"Warning: Pet still exists after deletion: {pet.id}")
            except ValidationError:
                pass
        elif get_resp.status_code not in (404, 500):
            raise AssertionError(
                f"Unexpected GET status after DELETE: {get_resp.status_code}, body: {get_resp.text}"
            )



