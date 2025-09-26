from requester.requester import CustomRequester
from utils.endpoints import PET_ENDPOINT

class PetApi(CustomRequester):
    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def add_pet(self, pet_data, expected_status=None):
        """POST /pet — создаём питомца"""
        return self.send_request(
            method="POST",
            endpoint=PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def update_pet(self, pet_data, expected_status=None):
        """PUT /pet — обновляем питомца"""
        return self.send_request(
            method="PUT",
            endpoint=PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def create_pet(self, pet_data, expected_status=None):
        return self.send_request(
            method="POST",
            endpoint=PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def get_pet_by_id(self, pet_id, expected_status=None):
        """GET /pet/{petId} — получение питомца по ID"""
        return self.send_request(
            method="GET",
            endpoint=f"{PET_ENDPOINT}/{pet_id}",
            expected_status=expected_status
        )

    def delete_pet(self, pet_id, expected_status=None):
        """DELETE /pet/{petId} — удаление питомца по ID"""
        return self.send_request(
            method="DELETE",
            endpoint=f"{PET_ENDPOINT}/{pet_id}",
            expected_status=expected_status,
        )