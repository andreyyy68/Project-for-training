import requests
import logging
import os

# Цвета для читаемости в логах
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class CustomRequester:
    """
    Кастомный реквестер для удобной работы с API:
    - стандартизирует отправку запросов
    - умеет логгировать запросы и ответы в curl-формате
    - опционально проверяет статус-коды
    """

    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, base_url: str, session):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()

        # Логгер
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        params: dict = None,
        expected_status: int | None = None,   # Теперь опционально
        need_logging: bool = True
    ) -> requests.Response:
        """Отправка HTTP-запроса"""

        url = f"{self.base_url}{endpoint}"

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=self.headers
        )

        if need_logging:
            self.log_request_and_response(response)

        # Проверяем статус-код только если передан expected_status
        if expected_status is not None and response.status_code != expected_status:
            raise AssertionError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response

    def log_request_and_response(self, response: requests.Response):
        """Логируем запрос и ответ в curl-формате"""

        try:
            request = response.request

            # Хедеры
            headers = " \\\n".join(
                [f"-H '{k}: {v}'" for k, v in request.headers.items()]
            )

            # Имя теста из pytest
            test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            # Тело запроса
            body = ""
            if request.body:
                try:
                    body = request.body.decode() if isinstance(request.body, bytes) else request.body
                except Exception:
                    body = str(request.body)
                body = f"-d '{body}' \n"

            # Лог запроса
            self.logger.info(
                f"{GREEN}{test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            # Лог ответа
            if not response.ok:
                self.logger.info(
                    f"\tRESPONSE:\nSTATUS_CODE: {RED}{response.status_code}{RESET}\n"
                    f"DATA: {RED}{response.text}{RESET}"
                )

        except Exception as e:
            self.logger.info(f"Logging failed: {type(e)} - {e}")
