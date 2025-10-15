import threading
from typing import Optional

_user_storage = threading.local()


def get_current_user():
    """Joriy so'rovdan foydalanuvchini qaytaradi (middleware orqali o'rnatiladi)."""
    return getattr(_user_storage, 'user', None)


class CurrentUserMiddleware:
    """Har bir so'rov uchun joriy foydalanuvchini thread-localda saqlaydi.

    AuthenticationMiddleware dan keyin ishlashi kerak.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_storage.user = getattr(request, 'user', None)
        try:
            response = self.get_response(request)
        finally:
            # Memory leaklarning oldini olish uchun tozalaymiz
            _user_storage.user = None
        return response
