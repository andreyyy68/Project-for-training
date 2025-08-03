import pytest
import requests

from api.api_manager import ApiManager

# Создаем сессии и закрываем их после тестов
@pytest.fixture
def create_api_client():
    clients = []

    def new_client():
        session = requests.Session()
        api_client = ApiManager(session)
        clients.append(api_client)
        return api_client

    yield new_client

    for client in clients:
        client.close()


# Создаем админскую сессию
@pytest.fixture
def create_admin_client():
    pass

# Создаем сессию для продавца
@pytest.fixture
def create_seller():
    pass

# Создаем сессию для user
@pytest.fixture
def create_user():
    pass