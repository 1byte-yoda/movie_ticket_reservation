# SEAT_RESERVATION
SEAT_RESERVATION_ROUTES = [
    "/api/seat-reservation/create",
    "/api/seat-reservation/update",
    "/api/seat-reservation",
    "/api/seat-reservation/cancel",
]
SEAT_RESERVATION_LIST_ROUTES = ["/api/seat-reservations"]


# ACCOUNT
ACCOUNT_ROUTES = ["/api/account"]
ACCOUNT_LOGIN_ROUTES = [
    "/api/auth/login",
    "/api/account/update"
]
ACCOUNT_LOGOUT_ROUTES = ["/api/auth/logout"]
ACCOUNT_FRESH_TOKEN_ROUTES = ["/api/auth/refresh"]


# USER
USER_REGISTER_ROUTES = ["/api/user/register"]
USER_ROUTES = ["/api/user/delete"]


# CINEMA
CINEMA_ROUTES = [
    "/api/cinema/<int:cinema_id>"
]
CINEMA_USER_ROUTES = [
    "/api/cinema/register",
    "/api/cinema/<int:cinema_id>/edit",
    "/api/cinema/delete"
]


# SCREEN
SCREEN_LIST_ROUTES = ["/api/cinema/<int:cinema_id>/screens"]
SCREEN_ROUTES = [
    "/api/cinema/<int:cinema_id>/screen/add",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/delete",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/edit",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>"
]


# MOVIE_SCREEN
MOVIE_SCREEN_ROUTES = [
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/add",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/delete",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/<int:movie_screen_id>",
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screen/<int:movie_screen_id>/edit"
]
MOVIE_SCREEN_LIST_ROUTES = [
    "/api/cinema/<int:cinema_id>/screen/<int:screen_id>/movie-screens"
]


# MOVIE
MOVIE_ROUTES = [
    "/api/cinema/<int:cinema_id>/movie/<int:movie_id>",
    "/api/cinema/<int:cinema_id>/movie/add",
    "/api/cinema/<int:cinema_id>/movie/<int:movie_id>/edit",
    "/api/cinema/<int:cinema_id>/movie/<int:movie_id>/delete"
]


# IMAGE UPLOAD
IMAGE_UPLOAD_ROUTES = [
    "/api/upload/image"
]