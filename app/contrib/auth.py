from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class AuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=username)
        return user
