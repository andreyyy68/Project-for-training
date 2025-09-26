# Базовые эндпоинты для User API
CREATE_USER_ENDPOINT = "/user"          # POST /user
GET_USER_BY_NAME_ENDPOINT = "/user/{username}"  # GET /user/{username}
LOGIN_USER_ENDPOINT = "/user/login"   # GET /user/login?username&password
LOGOUT_USER_ENDPOINT = "/user/logout" # GET /user/logout (если понадобится)
STORE_INVENTORY_ENDPOINT = "/store/inventory"
STORE_ORDER_ENDPOINT = "/store/order"
PET_ENDPOINT = "/pet"