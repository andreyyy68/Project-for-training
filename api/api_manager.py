# api/api_manager.py
from api.endpoints.user_api import UserAPI
from api.endpoints.sotre_api import StoreAPI
from api.endpoints.pet_api import PetApi
from utils.config import BASE_URL

class ApiManager:
    """
    Объединяет все API-классы с одной сессией.
    """

    def __init__(self, session):
        self.user_api = UserAPI(session=session, base_url=BASE_URL)
        self.store_api = StoreAPI(session=session, base_url=BASE_URL)
        self.pet_api = PetApi(session=session, base_url=BASE_URL)
