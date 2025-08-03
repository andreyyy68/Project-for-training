# Импорты эндпоинтов

class ApiManager:
    def __init__(self, session):
        self.session = session

    def close_session(self):
        self.session.close()
