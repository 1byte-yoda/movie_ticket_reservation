SEAT_RESERVATION_ROUTES = [
    "/api/seat-reservation/create",
    "/api/seat-reservation/update",
    "/api/seat-reservation",
    "/api/seat-reservation/cancel",
]
SEAT_RESERVATION_LIST_ROUTES = ["/api/seat-reservations"]

ACCOUNT_ROUTES = ["/api/account"]
ACCOUNT_LOGIN_ROUTES = ["/api/auth/login", "/api/account/update"]
ACCOUNT_LOGOUT_ROUTES = ["/api/auth/logout"]

USER_REGISTER_ROUTES = ["/api/user/register"]
USER_ROUTES = ["/api/user/delete"]

CINEMA_ROUTES = ["/api/cinema/<int:cinema_id>"]
CINEMA_USER_ROUTES = ["/api/cinema/register", "/api/cinema/delete"]

SCREEN_LIST_ROUTES = ["/api/cinema/<int:cinema_id>/screens"]
SCREEN_ROUTES = [
    "/api/cinema/<int:cinema_id>/screen/add",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/delete",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/edit"
]
