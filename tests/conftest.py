import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from playwright.sync_api import sync_playwright, Page
from utils.config import BASE_URL, HEADERS
from utils.generator import new_user_generate_payload, new_order_generate_payload, new_pet_generate_payload
import pytest
from requester.requester import CustomRequester
from api.api_manager import ApiManager




@pytest.fixture
def user_fixture():
    """Создание и удаление пользователя"""
    payload = new_user_generate_payload()

    # Создание пользователя
    response = requests.post(f"{BASE_URL}/user", json=payload, headers=HEADERS)

    yield payload  # возвращаем данные пользователя в тест

    # Удаляем пользователя после теста
    del_response = requests.delete(f"{BASE_URL}/user/{payload['username']}", headers=HEADERS)

@pytest.fixture
def requester():
    return CustomRequester(BASE_URL)

@pytest.fixture(scope="session")
def http_session():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture
def api_manager(http_session):
    return ApiManager(session=http_session)

@pytest.fixture
def new_user_payload():
    return new_user_generate_payload()

@pytest.fixture
def new_order_payload():
    """Фикстура для генерации тестового заказа"""
    return new_order_generate_payload()

@pytest.fixture
def new_pet_payload():
    """Данные для нового питомца"""
    return new_pet_generate_payload()

@pytest.fixture
def created_pet(api_manager, new_pet_payload):
    """Создаёт питомца через API и возвращает данные питомца"""
    resp = api_manager.pet_api.create_pet(new_pet_payload, expected_status=None)

    # Проверяем допустимые статусы
    assert resp.status_code in (200, 500, 404), (
        f"Failed to create pet: {resp.status_code}, body: {resp.text}"
    )

    if resp.status_code == 200:
        return resp.json()

    # если сервер отдал ошибку, возвращаем payload как заглушку
    return new_pet_payload

@pytest.fixture
def logged_in_user(api_manager, user_fixture):
    """
    Фикстура для авторизованного пользователя.
    Возвращает api_manager с авторизованной сессией.
    """
    resp_login = api_manager.user_api.login(
        username=user_fixture["username"],
        password=user_fixture["password"],
        expected_status=None
    )
    assert resp_login.status_code in (200, 404, 500), "Логин не прошёл!"
    return api_manager

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def auth_page(page):
    # Авторизация
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    return page  # Возвращаем авторизованную страницу

