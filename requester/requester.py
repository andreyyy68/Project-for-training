from utils.logger import get_logger

class CustomRequester:
    """
    Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов.
    """
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.logger = get_logger("CustomRequester")

    def send_request(self, method, endpoint, data=None, expected_status=200, params=None, need_logging=True):
        url = f"{self.base_url}{endpoint}"

        if need_logging:
            self.logger.info(f"Отправка запроса: {method.upper()} {url}")
            self.logger.debug(f"Headers: {self.headers}")
            self.logger.debug(f"Params: {params}")
            self.logger.debug(f"Payload: {data}")

        response = self.session.request(method, url, json=data, params=params, headers=self.headers)

        if need_logging:
            self.logger.info(f"Ответ [{response.status_code}] от {url}")
            self.logger.debug(f"Response Body: {response.text}")

        if response.status_code != expected_status:
            self.logger.error(f"Ожидался статус {expected_status}, но получен {response.status_code}")
            raise AssertionError(f"Expected {expected_status}, got {response.status_code}")

        return response
