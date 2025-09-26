from requester.requester import CustomRequester
from utils.endpoints import STORE_INVENTORY_ENDPOINT, STORE_ORDER_ENDPOINT

class StoreAPI(CustomRequester):
    def __init__(self, session, base_url):
        super().__init__(session=session, base_url=base_url)

    def get_inventory(self, expected_status=None):
        """GET /store/inventory"""
        return self.send_request(
            method="GET",
            endpoint=STORE_INVENTORY_ENDPOINT,
            expected_status=expected_status
        )

    def create_order(self, order_data, expected_status=None):
        """POST /store/order"""
        return self.send_request(
            method="POST",
            endpoint=STORE_ORDER_ENDPOINT,
            data=order_data,
            expected_status=expected_status
        )

    def get_order_by_id(self, order_id, expected_status=None):
        """GET /store/order/{orderId}"""
        return self.send_request(
            method="GET",
            endpoint=f"{STORE_ORDER_ENDPOINT}/{order_id}",
            expected_status=expected_status
        )

    def delete_order(self, order_id, expected_status=None):
        """DELETE /store/order/{orderId}"""
        return self.send_request(
            method="DELETE",
            endpoint=f"{STORE_ORDER_ENDPOINT}/{order_id}",
            expected_status=expected_status
        )